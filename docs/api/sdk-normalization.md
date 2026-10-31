# SDK normalization

[API overview](../api-notes.md) · [HTTP field reference](../api-schemas.md)

The HTTP reference describes raw request and response values. cosplay2py applies
the following conversions when exposing Python objects:

| HTTP representation | SDK representation |
|---|---|
| `message: "ok"` alongside an object payload | Marker removed before payload validation |
| Payload under an endpoint-specific key such as `comments` | Inner value returned by the resource method |
| UTC timestamp string, Unix seconds or Unix milliseconds | Timezone-aware `datetime` through `UTCDateTime` |
| `DD.MM.YY HH:MM` display string | Naive `datetime` through `LocalDateTime` |
| JSON inside a string | Decoded value through `JsonEncoded` |
| Empty optional enum string | `None` through `EmptyAsNone` |
| Numeric flag | Python `bool` for modeled boolean fields |
| Numeric decimal value | `Decimal` for modeled decimal fields |

Models preserve unknown extra fields. Optional fields commonly default to `None`;
some collection fields default to an empty list. Those defaults are library behavior,
not evidence that the server supplies a default or always returns the field.

The HTTP field reference uses aliases rather than Python attribute names. For example,
`RequestDetails.request_sections` reads the HTTP key `reqsections`, `values` reads
`reqvalues`, and `edit_enabled` reads `editEnabled`. Some role attributes read `ER`.
Inspect the [model definitions](../../src/cosplay2py/models) for the complete mapping.

Sync and async resource methods share request serialization. Their request builders
are a source of documented caller behavior; they do not establish server validation
rules or token permissions. The [endpoint reference](index.md) links supported SDK
methods beside their HTTP operations.
