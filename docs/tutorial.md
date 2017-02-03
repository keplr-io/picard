# Hunting for neural network architectures with Picard

Consider the following somewhat common neural network structure

```
Input -> Embedding -> LSTM -> [ Some dense layers ] -> [Dense layer before output] -> Output
```

Which is a simple variation of what [fchollet](http://) teaches you to build in keras in the keras docs [here](http://).

Suppose you're trying to use a model like this on a real world dataset. There are two immediate natural questions:


1. How well do we expect this model to work?
2. What do we do if it doesn't work well? How can we make it better?

The former you can answer by training and testing on your dataset. The intention of this note is to shed some light on the latter.

Among other things, here are some natural questions we might ask a model that roughly looks like the picture above:

- How many fully connected (dense) layers should we have?
- What should the activation functions be?
- Should we use dropout? With what probability?
- Loss function? Learning rate

The accurate and performant model we're looking for lies somewhere in the product space of all these choices. Schematically,  something like

![eq](https://cloud.githubusercontent.com/assets/5866348/22576891/599fa5da-e973-11e6-8269-7934096c8720.png)


How does one go about evaluating models with parameters living in this potentially high dimensional space?

We built [Picard](http://) to easily set up experiments that systematically answer questions like this, taking advantage of previous works on hyperparameter optimization by others. The remainder of tutorial walks you through setting up picard to explore a model space similar to the one described above.

## 1. The Graph

I'm just write a couple of lines to reproduce the rough architecture I outlined above as some edges in a graph labelled by an operator

```json
{
    "edges": [
        {
            "source": "input",
            "target": "post-embedding",
            "operator": "embedding"
        },
        {
            "source": "post-embedding",
            "target": "post-lstm",
            "operator": "lstm"
        },
        {
            "source": "post-lstm",
            "target": "post-ff",
            "operator": "feedforward"
        },
        {
            "source": "post-ff",
            "target": "output",
            "operator": "finalDense"
        }
    ],
}
```

This looks like

![graaaph](https://cloud.githubusercontent.com/assets/5866348/22577084/8a397ed6-e974-11e6-90e2-7158e5c0db47.png)

I'm also going to describe the legs of the model graph - inputs and outputs. The format is

```js
{
    "legs": {
        "in": {
            <inputLegKey>: <inputLayerSpec>,
            ...
        },
        "out": {
            <outputLegKey>: <outputLegSpec>,
            ...
        }
    }
}
```


Where inputLegKey, inputLayerSpec are respectively the name and options used to initialize an Input layer in keras. Similarly, the "out" field configures the "Output" layers in keras. For now let's use the cofiguration:


```js
{
    "legs": {
        "out": {
            "output": {
                "loss": "binary_crossentropy"
            }
        },
        "in": {
            "input": {}
        }
    }

}
```

## 2. Operators

Each "operator" label on the edge corresponds to an entry we're going to write in the "operators" field. Some of these are just configurations for keras layers

```json
{
    "operators": {
        "lstm": {
            "layer": "LSTM",
            "config": {
                "output_dim": 32
            }
        },
        "embedding": {
          "layer": "Embedding",
          "config": {
            "output_dim": 512,
            "dropout": 0.2,
            "input_dim": 10000,
            "input_length": 500
          }
        }
    }
}
```

**Our first hyperparameter**

Let's meet our first hyperparameter. For the final dense layer, I'm not really sure which activation to choose. Hence I'm going to declare it as a hyperparameter of my model space, with the `&choice` operation:

```json
{
    "operators": {
        ...,
        "finalDense": {
            "layer": "Dense",
            "config": {
                "output_dim": 1,
                "activation": {
                    "&choice": {
                        "options": [
                          "relu",
                          "sigmoid",
                          "softmax"
                        ]
                    }
                }
            }
        }
    }
}
```


Just to be completely clear, this means for each trial in our experiment, the above spec will evaluate the `"activation"` field to one of the strings `"relu", "sigmoid", "softmax"`. The exact choice is suggested by the optimization algorithm you configure in hyperopt.


**More hyperspecs: the feedforward chunk**

Let's write the stack of dense layers in picard. Picard has a shorthand, `"#repeat"`, for repeating things:

```json
{
    "operators": {
        ...,
        "feedforward": {
            "#repeat": 3,
            "operator": {
                "layer": "Dense",
                "config": {
                  "output_dim": 512,
                  "activation": {
                    "&choice": {
                      "options": [
                        "relu",
                        "sigmoid"
                      ]
                    }
                  }
                }
            }
        }
    }
}
```

This tells it to compose that operator with a copy of itself 3 times.

As a side note, observe we snuck another hyperspec in there: the same `&choice` we just used above for the final dense layer. All picard operations (we've met hyperopt operations like `&choice` and operator operation `#repeat` so far) can be arbitrarily nested.

The `#repeat` operator is useful because now we can make the `times` argument a hyperparameter.

For the sake of saving some time, let me give the full operator configuration for this feed forward portion of our neural net now

```json
{
    "operators": {
        ...,
        "feedforward": {
          "#repeat": {
            "operator": {
              "#compose": [
                {
                  "layer": "Dense",
                  "config": {
                    "output_dim": 512,
                    "activation": {
                      "&choice": {
                        "options": [
                          "relu",
                          "sigmoid"
                        ]
                      }
                    }
                  }
                },
                {
                  "#optional": {
                    "layer": "Dropout",
                    "config": {
                      "p": {
                        "&uniform": {
                          "high": 0.6,
                          "low": 0.3
                        }
                      }
                    }
                  }
                }
              ]
            },
            "+times": {
              "&choice": {
                "options": [
                  2,
                  3,
                  4,
                  5
                ]
              }
            }
          }
        }
    }
}
}
```

This contains some new operators

- `#compose` just takes a list of operators and apply them one after the other
- `#optional` marks an item on a list as optional - i.e. it lets hyperopt choose whether to include that element

Feel free to spend some time making sense of the configuration above. In short it says something like:

"Repeat a dense layer, with one of the possible activations, possibly followed by a dropout, of probability between 0.3 to 0.6, between 2 and 5 times."

Paired with the configuration of the edges and legs above, this completes our configuration of the model space. But hyperparameters in deep learning are not only parameters in the model - there are also parameters associated with how one trains the model. Here we're going to take the following:

```
{
    "compile": {
      "optimizer": {
        "&choice": {
          "options": [
            "rmsprop",
            "adam"
          ]
        }
      }
    },

    "fit": {
      "batch_size": {
        "&choice": {
          "options": [
            16,
            32
          ]
        }
      }
    },
}
```

The compile field configures the arguments of the Keras "compile" function, and "fit" configures parameters passed to the keras "fit" function. Picard gives us a declarative interface to set all these parameters to be used in a keras experiment, and furthermore lets us convert these values into hyperparameters in our experiment.


## Launching the experiment

We just walked through converting our idea of a model into a space of hyperparameters, specified by a picard configuration. Picard takes this configuration and runs the experiment for you. Launching the experiment is a single function call.

```python
from picard.minimizer import get_min_model
from picard.util.data import get_picard_input
from hyperopt import Trials
import numpy as np

min_model = get_min_model(
    spec= {
        ...
    },
    data=get_picard_input(
        dataspec, {
            'myInputFieldName': np.loadtxt('./datain.csv'),
            'myOutputFieldName': np.loadtxt('./dataout.csv')
        }
    ),
    trials=Trials(),
    max_evals=15
)

```

We didn't mention much the "data" field in this tutorial. It's a specification of how your input dataset should map to legs of the model. Head over to the docs to learn the details.

## Extra goodies

- Picard configs can be long and it could be easy to make a typo. We built a little tool, configVis, for validating your syntax

![validator](https://cloud.githubusercontent.com/assets/5866348/22577241/4da49194-e975-11e6-9892-fb00c305addb.png)


- You can't get around the problem of needing many many evaluations of an expensive objective function when doing hyperparameter optimization. We built a platform around picard to let you run your picard experiments in the cloud with many machines working in parallel. Furthermore training metrics from these cloud experiments are streamed in realtime to a [hera](http://) dashboard.

![dash](https://cloud.githubusercontent.com/assets/5866348/22577386/38d27be0-e976-11e6-83bc-af4a4f07b3ce.png)

The picard runner is currently in private beta - sign up [here](http://) if you want to give it a spin!

(

    Footnote for pedants (like me):

- Product space = product topological space, you don't expect finite set to form vector spaces.

- In the problem outline here we have some product of finite sets and 1 or 2 parameters that lay in finite intervals. The product looks something like a collection of disjoint boxes. Endowing this with the obvious charts it has finite dimension. Doesn't make the problem less tedious though - you have expensive evaluations at each point. The size of the finite dimension (products of finite parameters) can get large fast.

- In machine learning people like to draw architecture graphs with nodes being layers. One can notice the graphs in Picard are the opposite/dual of these - layers are edges, domain and ranges of layers are nodes. In practice this enables picard specs to associate arbitrarily complicated operators to edges, with no ambiguity about how to execute the computation graph. Also personally to me this is the natural way to think about associating spaces and operators to a graph - look at graphs as small categories with vertices as objects, and try to build functors from this category.

)
