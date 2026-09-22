# NFA to DFA and DFA Minimization Web Server

Formal Languages (SI2002) — EAFIT University

This server has two parts: DFA minimization (Assignment 2, documented first) and
NFA to DFA conversion (Assignment 1, documented at the end).

## Authors

- Camilo Estrada — TODO: full name
- Mariana Salomé Velásquez Gallego

Class number: TODO

## Environment

- Operating system: Windows 11 (build 10.0.26100)
- Language: Python 3.12 (TODO: exact version, run `python --version`)
- Framework: Flask (TODO: exact version, run `pip show flask`)
- Testing tools: curl, `unittest` (included with Python)

## How to run

Install the only dependency:

```
pip install flask
```

Start the server:

```
python app.py
```

The server starts at http://127.0.0.1:5000

## Endpoint: `POST /minimize`

Receives one or more DFAs with no inaccessible states and returns, for each one,
the pairs of equivalent states.

### How the DFA is sent

The body of the request is **plain text** with the same format as the assignment
statement:

1. A line with `c > 0`, the number of cases.
2. For each case:
   1. A line with `n > 0`, the number of states. States are `0 .. n-1` and the initial state is always `0`.
   2. A line with the alphabet, letters `a-z` separated by spaces.
   3. A line with the final states separated by spaces (the line is empty if there are none).
   4. `n` lines, one per state. Each line starts with the state number, followed by
      the destination state for each symbol, in the same order as the alphabet.

Example: the 6-state DFA of the statement. Save it as `input.txt`:

```
1
6
a b
1 4 5
0 1 2
1 3 4
2 4 3
3 5 5
4 5 5
5 5 5
```

Send it with curl (in PowerShell use `curl.exe`, since `curl` is an alias):

```
curl.exe -X POST http://127.0.0.1:5000/minimize -H "Content-Type: text/plain" --data-binary "@input.txt"
```

### Response

A JSON object with one entry per case, in the same order as the input. Each entry
lists the equivalent pairs `[p, q]` with `p < q`, sorted lexicographically:

```
{"cases": [{"equivalent_pairs": [[4, 5]]}]}
```

If a DFA has no equivalent states, its list is empty: `{"equivalent_pairs": []}`.

### Errors

If the input is malformed (missing lines, non-numeric values, a symbol that is not
a letter, states out of range, etc.) the server answers `400 Bad Request` with a
message that explains the problem:

```
{"error": "Case 1, row 0: expected 3 numbers, got 2"}
```

## The minimization algorithm

We implement the table-filling algorithm from Kozen (1997), Lecture 14, which is
based on the construction of Lecture 13.

Two states `p` and `q` are **equivalent** if no string tells them apart:
for every string `x`, `δ(p, x)` is final if and only if `δ(q, x)` is final.
If some string `x` does tell them apart, the pair is **distinguishable**.
The algorithm marks every distinguishable pair; the pairs that stay unmarked are
exactly the equivalent ones.

1. **Build the table.** Create an entry for every pair `{p, q}` with `p < q`, all unmarked.
2. **Mark final vs. non-final.** Mark `{p, q}` if exactly one of them is final.
   They are told apart by the empty string.
3. **Propagate.** Repeat until nothing changes: if an unmarked pair `{p, q}` has a
   symbol `a` such that `{δ(p, a), δ(q, a)}` is already marked, mark `{p, q}`.
   If `x` tells the two destinations apart, then `a·x` tells `p` and `q` apart.
4. **Read the result.** `p` and `q` are equivalent if and only if `{p, q}` was never marked.

Example with the DFA of the statement (`F = {1, 4, 5}`):

- Step 2 marks the 9 pairs that mix a final and a non-final state.
- The first pass of step 3 marks `{0,3}`, `{1,4}`, `{1,5}` and `{2,3}`.
- The second pass marks `{0,2}`. The third pass changes nothing, so it stops.
- Only `{4, 5}` is left unmarked, so states 4 and 5 are equivalent and can be collapsed.

## How it was integrated into the Assignment 1 server

The new feature was added to the same Flask application of Assignment 1, without
changing the existing code:

- `minimizer.py` (new) holds the algorithm. The function `equivalent_pairs(delta, finals)`
  has no knowledge of Flask or of the input format.
- `parser.py` (new) turns the plain-text body into the values that `equivalent_pairs` needs
  and raises an error with a clear message when the input is malformed.
- `app.py` only gets the new route `/minimize`: it parses the body, calls
  `equivalent_pairs` for each case, builds the JSON response and returns `400` on malformed input.

The Assignment 1 endpoints `POST /convert` (NFA to DFA) and `POST /simulate` keep working as before; they are documented at the end of this file.

## Tests

The algorithm has its own unit tests (the example of the statement, a single state,
a one-letter alphabet, an already minimal DFA, several equivalent pairs, output order):

```
python -m unittest test_minimizer -v
```

## Assignment 1: NFA to DFA (unchanged)

The endpoints `POST /convert` and `POST /simulate` receive JSON and are documented below.

### Input format

Epsilon transitions are written with the reserved symbol "eps":

```
{"from": "q3", "to": "q1", "symbol": "eps"}
```

### Algorithm

This server converts a Nondeterministic Finite Automaton (NFA) into an
equivalent Deterministic Finite Automaton (DFA) using the Subset
Construction Algorithm.

Epsilon-closure: given a state (or a set of states), it finds every other state reachable using only epsilon transitions, which do not consume any input symbol.
Move: given a set of states and one symbol, it finds every state reachable by consuming that symbol.
To build the DFA, we start from the epsilon-closure of the NFA's initial state. For each DFA state and each symbol in the alphabet, we apply move and then epsilon-closure to get the next DFA state. We repeat this until no new states appear. A DFA state is accepting if the set of NFA states it represents contains at least one accepting state of the original NFA.

If no transition is defined for a given state and symbol, the DFA has no outgoing edge for that pair, and any input string requiring that transition is rejected.

### Examples

#### POST /convert

Request:

```
{
    "states": ["q0", "q1", "q2", "q3"],
    "alphabet": ["a", "b", "c"],
    "initial": "q0",
    "accepting": ["q2"],
    "transitions": [
        {"from": "q0", "to": "q3", "symbol": "b"},
        {"from": "q3", "to": "q1", "symbol": "eps"},
        {"from": "q3", "to": "q2", "symbol": "eps"},
        {"from": "q1", "to": "q2", "symbol": "c"},
        {"from": "q1", "to": "q2", "symbol": "eps"},
        {"from": "q2", "to": "q3", "symbol": "a"}
    ]
}
```

Response:

```
{
    "dfaStates": ["q0", "q1q2q3", "q2"],
    "transitions": [
        {"from": "q0", "symbol": "b", "to": "q1q2q3"},
        {"from": "q1q2q3", "symbol": "a", "to": "q1q2q3"},
        {"from": "q1q2q3", "symbol": "c", "to": "q2"},
        {"from": "q2", "symbol": "a", "to": "q1q2q3"}
    ],
    "acceptingStates": ["q1q2q3", "q2"]
}
```

#### POST /simulate

Request:

```
{
    "dfa": {
        "dfaStates": ["q0", "q1q2q3", "q2"],
        "transitions": [
            {"from": "q0", "symbol": "b", "to": "q1q2q3"},
            {"from": "q1q2q3", "symbol": "a", "to": "q1q2q3"},
            {"from": "q1q2q3", "symbol": "c", "to": "q2"},
            {"from": "q2", "symbol": "a", "to": "q1q2q3"}
        ],
        "acceptingStates": ["q1q2q3", "q2"]
    },
    "input": "bc"
}
```

Response:

```
{
    "path": ["q0", "q1q2q3", "q2"],
    "accepted": true
}
```
"# Formales" 
