# Picard Syntax

## TL;DR

- `&blah` is a **hyperopt operation**. Some available ones

    + `&choice`
    + `&randint`
    + `&uniform`

    and anything else available in hyperopt

- `#blah` is a **operator composition spec**. Currently there are two such specs available

    + `#compose` specifies layer (operator) composition

            ```

                '#compose': {
                    'operators': [
                        'layer1',
                        'layer2'
                    ]
                }

            ```


    + `#repeat` composes an operator with itself a number of times


            ```

                '#repeat': {
                    'operator': 'layer',
                    'times': 5
                }

            ```

- `@blah` is a **graph operation** which induces a topology change on the model graph. This part of the documentation will be improved once we have more useful graph operators.

## A few words on the syntax

The syntax is inspired by BSON, but more so inspired by the [React immutability helpers](https://facebook.github.io/react/docs/update.html). The difference between the 2 is

- BSON syntax:


```

    {
        [operator]: {
            [fieldName]: [operatorSpecs]
        }
    }

```

- Update syntax

```

    {
        [fieldName]: {
            [operator]: [operatorSpec]
        }
    }

```

Picard uses the latter. The former is optimized for batch-updatig, as one might want when querying a database. But the latter is cleaner: the operator spec is read off as a single object, and the operators largely preserve the structure of the object tree.