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
