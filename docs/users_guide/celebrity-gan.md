[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

<!--
<a href="https://singularitynet.io/">
<img align="right" src="../assets/logo/singularityNETblue.png" alt="drawing" width="160"/>
</a>
-->

# Celebrity GAN

This service uses convolutional neural networks to generate imaginary celebrities from random seeds.

It is part of SingularityNET's third party services, [originally implemented by tkarras](https://github.com/tkarras/progressive-growing-of-gans).

### Welcome

The service takes as input a random seed (integer): a random integer from 0 to 4294967295 that serves as a seed for generating a celebrity. It will then return a base64 encoded image and the chosen or randomly generated seed (so that the results are reproducible).

### What’s the point?

This service can be used to generate faces of imaginary celebrities that may serve as example avatars or just for fun.

### How does it work?

To get a response from the service, the only input necessary is an integer number from 0 to 4294967295. If not provided, the service will generate it randomly.

You can use this service at [SingularityNET DApp](http://beta.singularitynet.io/) by clicking on `snet/celebrity-gan`.

You can also call the service from SingularityNET CLI:

```
$ snet client call snet celebrity-gan generate_celebrity '{"seed": 13}'
```

Go to [this tutorial](https://dev.singularitynet.io/tutorials/publish/) to learn more about publishing, using and deleting a service.

### What to expect from this service?

Example:

**Input**

- seed: 13

**Output**

- data:
<img width="100%" src="assets/examples/example_output.png">

- seed: 13