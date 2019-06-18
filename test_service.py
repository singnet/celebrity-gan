import grpc

# import the generated classes
import service.service_spec.celebrity_gan_pb2_grpc as grpc_bt_grpc
import service.service_spec.celebrity_gan_pb2 as grpc_bt_pb2

from service import registry

if __name__ == "__main__":
    print("Started test script")
    try:
        # open a gRPC channel
        endpoint = "localhost:{}".format(registry["celebrity_gan_service"]["grpc"])
        channel = grpc.insecure_channel("{}".format(endpoint))
        print("Opened channel")

        # setting parameters
        grpc_method = "generate_celebrity"
        random_seed = 0

        # create a stub (client)
        stub = grpc_bt_grpc.GenerateCelebrityStub(channel)
        print("Stub created.")

        # create a valid request message
        request = grpc_bt_pb2.RandomSeed(seed=random_seed)

        # make the call
        response = stub.generate_celebrity(request)

        if response.data:
            print("Response received. Random seed used: {}".format(response.data[0:100]))
            print("First 100 characters of base64 image: {}".format(response.data[0:100]))
            print("Service successfully completed!")
            exit(0)
        else:
            print("Service failed! No data received.")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)
