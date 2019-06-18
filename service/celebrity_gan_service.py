import os
import logging
import grpc
import service.service_spec.celebrity_gan_pb2_grpc as grpc_bt_grpc
from service.service_spec.celebrity_gan_pb2 import Image
from service import registry, tfutil
import concurrent.futures as futures
import sys
import argparse
import time
import pickle
import numpy as np
import tensorflow as tf
from multiprocessing import Pool
import PIL.Image
from io import BytesIO
import base64

logging.basicConfig(
    level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s"
)
log = logging.getLogger("celebrity_gan_service")


class GenerateCelebrityServicer(grpc_bt_grpc.GenerateCelebrityServicer):
    """GenerateCelebrity servicer class to be added to the gRPC stub.
    Derived from protobuf (auto-generated) class."""

    def __init__(self):
        log.debug("GenerateCelebrityServicer created!")
        self.model_path = '/opt/singnet/celebrity-gan/service/Gs.pkl'
        self.result = Image()

    def generate_celebrity(self, request, context):
        """Receives gRPC request, parses JSON and adds a new field before returning the same JSON message."""

        if request:  # If correctly received a non-empty request
            if request.seed == 0:
                random_seed = np.random.randint(low=0, high=4294967295)
            else:
                random_seed = request.seed
            with Pool(1) as p:
                image = p.apply(self._generate_celebrity, (random_seed,))
                pil_img = PIL.Image.fromarray(image)
                buff = BytesIO()
                pil_img.save(buff, format="PNG")
                self.result.data = base64.b64encode(buff.getvalue()).decode("utf-8")
                self.result.seed = random_seed
                return self.result
        else:
            log.error("Did not receive a valid request.")
            exit(1)

    def _generate_celebrity(self, random_seed):
        # Import official CelebA-HQ networks.
        with open(self.model_path, 'rb') as file:
            session = tf.InteractiveSession()
            Gs = pickle.load(file)
            # Generate latent vectors.
            latents = np.random.RandomState(random_seed).randn(1, *Gs.input_shapes[0][1:])  # 1000 random latents
            # Generate dummy labels (not used by the official networks).
            labels = np.zeros([latents.shape[0]] + Gs.input_shapes[1][1:])

            # Run the generator to produce a set of images.
            images = Gs.run(latents, labels)

            # Convert images to PIL-compatible format.
            images = np.clip(np.rint((images + 1.0) / 2.0 * 255.0), 0.0, 255.0).astype(np.uint8)  # [-1,1] => [0,255]
            images = images.transpose(0, 2, 3, 1)  # NCHW => NHWC
            session.close()
            return images[0]


def serve(max_workers=5, port=7777):
    """The gRPC serve function.

    Params:
    max_workers: pool of threads to execute calls asynchronously
    port: gRPC server port

    Add all your classes to the server here.
    (from generated .py files by protobuf compiler)"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_GenerateCelebrityServicer_to_server(
        GenerateCelebrityServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


def common_parser(script_name):
    parser = argparse.ArgumentParser(prog=script_name)
    service_name = os.path.splitext(os.path.basename(script_name))[0]
    parser.add_argument(
        "--grpc-port",
        help="port to bind gRPC service to",
        default=registry[service_name]["grpc"],
        type=int,
        required=False,
    )
    return parser


def main_loop(grpc_handler, args):
    """From gRPC docs:
    Because start() does not block you may need to sleep-loop if there is nothing
    else for your code to do while serving."""
    server = grpc_handler(port=args.grpc_port)
    server.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    """Runs the gRPC server to communicate with the Snet Daemon."""
    parser = common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    main_loop(serve, args)
