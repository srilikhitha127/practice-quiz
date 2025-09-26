import streamlit as st
import random
import string
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Programming Quiz App", 
    page_icon="💻", 
    layout="wide"
)

# Quiz data
QUIZ_DATA = {
    "Python": {
        "Easy": [
            {
                "question": "What is the correct way to create a list in Python?",
                "options": ["list = []", "list = {}", "list = ()", "list = []"],
                "correct": 0,
                "hint": "Lists use square brackets and can be empty."
            },
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["function", "def", "func", "define"],
                "correct": 1,
                "hint": "Python uses 'def' followed by the function name."
            },
            {
                "question": "What does the 'print()' function do?",
                "options": ["Reads input", "Displays output", "Calculates math", "Creates variables"],
                "correct": 1,
                "hint": "Print displays text or variables to the console."
            }
        ],
        "Medium": [
            {
                "question": "What is the output of: print(3 * 2 ** 2)?",
                "options": ["12", "18", "36", "6"],
                "correct": 0,
                "hint": "Remember PEMDAS: Parentheses, Exponents, Multiplication, Division, Addition, Subtraction."
            },
            {
                "question": "Which method is used to add an item to the end of a list?",
                "options": ["append()", "add()", "insert()", "extend()"],
                "correct": 0,
                "hint": "append() adds a single item to the end of the list."
            },
            {
                "question": "What does 'len()' function return?",
                "options": ["The last element", "The length", "The sum", "The average"],
                "correct": 1,
                "hint": "len() returns the number of items in a sequence."
            }
        ],
        "Hard": [
            {
                "question": "What is the time complexity of list.append()?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                "correct": 0,
                "hint": "Appending to a list is constant time on average."
            },
            {
                "question": "What does this code output: [x**2 for x in range(3)]?",
                "options": ["[0, 1, 4]", "[1, 4, 9]", "[0, 1, 2]", "Error"],
                "correct": 0,
                "hint": "This is a list comprehension that squares each number from 0 to 2."
            },
            {
                "question": "Which is NOT a valid way to create a dictionary?",
                "options": ["dict()", "{}", "dict([('a', 1)])", "dict{key: value}"],
                "correct": 3,
                "hint": "Dictionary literals use curly braces with colons, not curly braces with colons in parentheses."
            }
        ]
    },
    "JavaScript": {
        "Easy": [
            {
                "question": "What is the correct way to declare a variable in JavaScript?",
                "options": ["var name = 'John'", "variable name = 'John'", "v name = 'John'", "declare name = 'John'"],
                "correct": 0,
                "hint": "JavaScript uses 'var', 'let', or 'const' to declare variables."
            },
            {
                "question": "Which operator is used for strict equality in JavaScript?",
                "options": ["==", "===", "=", "!="],
                "correct": 1,
                "hint": "=== checks both value and type equality."
            },
            {
                "question": "What does 'console.log()' do?",
                "options": ["Creates a log file", "Displays output", "Calculates math", "Reads input"],
                "correct": 1,
                "hint": "console.log() outputs messages to the browser console."
            }
        ],
        "Medium": [
            {
                "question": "What will this code output: console.log(typeof null)?",
                "options": ["'null'", "'object'", "'undefined'", "Error"],
                "correct": 1,
                "hint": "This is a known quirk in JavaScript - typeof null returns 'object'."
            },
            {
                "question": "Which method is used to add an element to the end of an array?",
                "options": ["push()", "add()", "append()", "insert()"],
                "correct": 0,
                "hint": "push() adds one or more elements to the end of an array."
            },
            {
                "question": "What does 'JSON.parse()' do?",
                "options": ["Converts object to string", "Parses JSON string", "Validates JSON", "Creates JSON"],
                "correct": 1,
                "hint": "JSON.parse() converts a JSON string into a JavaScript object."
            }
        ],
        "Hard": [
            {
                "question": "What is the output of: (function() { return this; })()?",
                "options": ["undefined", "window", "global", "null"],
                "correct": 1,
                "hint": "In non-strict mode, 'this' in a function refers to the global object (window in browsers)."
            },
            {
                "question": "What does 'hoisting' mean in JavaScript?",
                "options": ["Moving variables up", "Variable/function declarations are moved to top", "Lifting objects", "Raising errors"],
                "correct": 1,
                "hint": "Hoisting moves variable and function declarations to the top of their scope."
            },
            {
                "question": "Which is NOT a valid way to create an object?",
                "options": ["{}", "new Object()", "Object.create()", "object()"],
                "correct": 3,
                "hint": "There's no built-in 'object()' constructor function in JavaScript."
            }
        ]
    },
    "Java": {
        "Easy": [
            {
                "question": "What is the correct way to declare a variable in Java?",
                "options": ["int age = 25;", "var age = 25;", "age = 25;", "int age = 25"],
                "correct": 0,
                "hint": "Java requires explicit type declaration and semicolon at the end."
            },
            {
                "question": "Which keyword is used to create a class in Java?",
                "options": ["class", "Class", "create", "new"],
                "correct": 0,
                "hint": "Java uses lowercase 'class' keyword to define classes."
            },
            {
                "question": "What does 'public static void main(String[] args)' represent?",
                "options": ["A method", "A class", "A variable", "A package"],
                "correct": 0,
                "hint": "This is the main method where Java program execution begins."
            }
        ],
        "Medium": [
            {
                "question": "What is the output of: System.out.println(5 / 2)?",
                "options": ["2.5", "2", "2.0", "Error"],
                "correct": 1,
                "hint": "Integer division in Java truncates the decimal part."
            },
            {
                "question": "Which collection class is synchronized?",
                "options": ["ArrayList", "Vector", "LinkedList", "HashSet"],
                "correct": 1,
                "hint": "Vector is synchronized, making it thread-safe but slower."
            },
            {
                "question": "What does 'final' keyword do?",
                "options": ["Makes variable constant", "Ends program", "Creates loop", "Imports package"],
                "correct": 0,
                "hint": "final makes a variable constant and unchangeable."
            }
        ],
        "Hard": [
            {
                "question": "What is the time complexity of HashMap.get()?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                "correct": 0,
                "hint": "HashMap provides constant time average case for get operations."
            },
            {
                "question": "What does 'transient' keyword do?",
                "options": ["Makes variable temporary", "Excludes from serialization", "Creates thread", "Imports data"],
                "correct": 1,
                "hint": "transient excludes a variable from serialization process."
            },
            {
                "question": "Which is NOT a valid access modifier?",
                "options": ["public", "private", "protected", "internal"],
                "correct": 3,
                "hint": "Java has public, private, protected, and package-private (default), but not 'internal'."
            }
        ]
    }
}

# Category definitions for language selection UI
CATEGORY_TO_LANGUAGES = {
    "General-Purpose Languages": [
        "Python", "Java", "C++", "C#", "JavaScript", "Go", "Ruby", "Swift",
        "Kotlin", "Rust", "PHP", "R", "Perl", "Haskell", "Julia",
    ],
    "Markup and Styling Languages": [
        "HTML (HyperText Markup Language)",
        "CSS (Cascading Style Sheets)",
    ],
    "Database Query Languages": [
        "SQL (Structured Query Language)",
        "NoSQL",
    ],
    "Scripting Languages": [
        "Bash",
        "PowerShell",
    ],
}

# Helper to provide safe base for languages without specific banks
def _base_language(language: str) -> str:
    return language if language in QUIZ_DATA else "Python"

def _normalize_lang(language: str) -> str:
    name = (language or "").strip().lower()
    aliases = {
        "cpp": "c++",
        "c++": "c++",
        "c sharp": "c#",
        "c#": "c#",
        "js": "javascript",
        "javascript": "javascript",
        "py": "python",
        "python": "python",
        "java": "java",
        "golang": "go",
        "go": "go",
        "ruby": "ruby",
        "swift": "swift",
        "kotlin": "kotlin",
        "rust": "rust",
        "php": "php",
        "r": "r",
        "perl": "perl",
        "haskell": "haskell",
        "julia": "julia",
        "html (hypertext markup language)": "html",
        "html": "html",
        "css (cascading style sheets)": "css",
        "css": "css",
        "sql (structured query language)": "sql",
        "sql": "sql",
        "nosql": "nosql",
        "bash": "bash",
        "powershell": "powershell",
    }
    return aliases.get(name, name)

# Large neutral MCQ pool to avoid repeats on Easy level
def _neutral_easy_mcq(language: str) -> list:
    L = language
    items = [
        {"question": f"{L}: Which operator compares equality?", "options": ["=", "==", ":=", "=>"], "correct": 1, "hint": "Two equals."},
        {"question": f"{L}: Arrays/Lists are typically ____ indexed.", "options": ["0-based", "1-based", "2-based", "-1-based"], "correct": 0, "hint": "Starts at zero in many languages."},
        {"question": f"{L}: Which term means error during execution?", "options": ["syntax error", "runtime error", "compile-time error", "linker error"], "correct": 1, "hint": "Occurs while running."},
        {"question": f"{L}: Which structure stores key-value pairs?", "options": ["array", "map", "stack", "queue"], "correct": 1, "hint": "Associative."},
        {"question": f"{L}: Which loop is best for iterating a count?", "options": ["for", "while", "do-while", "switch"], "correct": 0, "hint": "Counter variable."},
        {"question": f"{L}: Which data type represents true/false?", "options": ["int", "string", "bool", "float"], "correct": 2, "hint": "Logical."},
        {"question": f"{L}: Which operator often concatenates strings?", "options": ["+", "-", "*", "/"], "correct": 0, "hint": "Overloaded in many languages."},
        {"question": f"{L}: A function inside a class is a ____.", "options": ["field", "method", "module", "macro"], "correct": 1, "hint": "Invoked on objects."},
        {"question": f"{L}: Which DS follows FIFO?", "options": ["stack", "queue", "set", "tree"], "correct": 1, "hint": "First-in, first-out."},
        {"question": f"{L}: Which DS follows LIFO?", "options": ["stack", "queue", "set", "tree"], "correct": 0, "hint": "Last-in, first-out."},
        {"question": f"{L}: Sorting ascending typically uses ____ sort built-in.", "options": ["custom", "library", "manual", "random"], "correct": 1, "hint": "Standard library."},
        {"question": f"{L}: Which notation describes time complexity?", "options": ["Sigma", "Theta", "Big-O", "Lambda"], "correct": 2, "hint": "Upper bound."},
        {"question": f"{L}: Which search on sorted arrays runs in O(log n)?", "options": ["linear", "binary", "hash", "dfs"], "correct": 1, "hint": "Divide and conquer."},
        {"question": f"{L}: Which DS provides O(1) average lookup?", "options": ["array", "linked list", "hash map", "binary tree"], "correct": 2, "hint": "Hashing."},
        {"question": f"{L}: Which loop executes body at least once?", "options": ["for", "while", "do-while", "foreach"], "correct": 2, "hint": "Condition checked after."},
        {"question": f"{L}: Which is a non-primitive numeric type?", "options": ["int", "float", "decimal", "bool"], "correct": 2, "hint": "High precision."},
        {"question": f"{L}: A collection with no duplicates is a ____.", "options": ["list", "queue", "set", "stack"], "correct": 2, "hint": "Mathematical term."},
        {"question": f"{L}: Which structure is hierarchical?", "options": ["graph", "tree", "queue", "stack"], "correct": 1, "hint": "Parent/child."},
        {"question": f"{L}: Which traversal uses a stack?", "options": ["BFS", "DFS", "Dijkstra", "Kruskal"], "correct": 1, "hint": "Depth-first."},
        {"question": f"{L}: Stable sort preserves ____ order.", "options": ["random", "relative", "reverse", "lexical"], "correct": 1, "hint": "Equal keys."},
        {"question": f"{L}: JSON is primarily a ____ format.", "options": ["binary", "text", "image", "audio"], "correct": 1, "hint": "Human-readable."},
        {"question": f"{L}: HTTP status 200 means ____.", "options": ["Not Found", "OK", "Redirect", "Server Error"], "correct": 1, "hint": "Success."},
        {"question": f"{L}: The modulus operator returns the ____.", "options": ["sum", "remainder", "quotient", "difference"], "correct": 1, "hint": "After division."},
        {"question": f"{L}: Which structure is First-In Last-Out?", "options": ["queue", "stack", "deque", "map"], "correct": 1, "hint": "Push/pop."},
        {"question": f"{L}: Which complexity is faster?", "options": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"], "correct": 3, "hint": "Smallest growth."},
        {"question": f"{L}: ASCII encodes characters using ____ bits originally.", "options": ["7", "8", "16", "32"], "correct": 0, "hint": "7-bit."},
        {"question": f"{L}: Which protocol secures HTTP?", "options": ["FTP", "TLS", "SSH", "SMTP"], "correct": 1, "hint": "HTTPS."},
        {"question": f"{L}: Which structure allows duplicates?", "options": ["set", "map", "multiset", "dictionary"], "correct": 2, "hint": "Multi- container."},
        {"question": f"{L}: Which statement is used to handle exceptions?", "options": ["if", "try", "switch", "goto"], "correct": 1, "hint": "Guard risky code."},
        {"question": f"{L}: Which DS is best for BFS frontier?", "options": ["stack", "queue", "list", "set"], "correct": 1, "hint": "FIFO."},
        {"question": f"{L}: Cache replacement policy: LRU stands for ____.", "options": ["Least Rarely Used", "Least Recently Used", "Last Recently Used", "Least Randomly Used"], "correct": 1, "hint": "Recency."},
    ]
    return items

def _neutral_medium_fill(language: str) -> list:
    L = language
    items = [
        {"q": f"{L}: Fill - First index in zero-based indexing is ___.", "a": "0", "hint": "Not one."},
        {"q": f"{L}: Fill - Structure storing key/value is a ___.", "a": "map", "hint": "Associative."},
        {"q": f"{L}: Fill - LIFO structure is a ___.", "a": "stack", "hint": "Opposite of queue."},
        {"q": f"{L}: Fill - FIFO structure is a ___.", "a": "queue", "hint": "First-in/First-out."},
        {"q": f"{L}: Fill - Equality comparison commonly uses ___.", "a": "==", "hint": "Double equals."},
        {"q": f"{L}: Fill - Algorithm complexity uses ____ notation.", "a": "Big-O", "hint": "Asymptotic."},
        {"q": f"{L}: Fill - Binary uses base ___.", "a": "2", "hint": "Two symbols."},
        {"q": f"{L}: Fill - A collection without duplicates is a ___.", "a": "set", "hint": "Mathematical term."},
        {"q": f"{L}: Fill - Sorting ascending uses ____ order.", "a": "increasing", "hint": "Opposite of decreasing."},
        {"q": f"{L}: Fill - An error at runtime is a ____ error.", "a": "runtime", "hint": "During execution."},
        {"q": f"{L}: Fill - A function parameter is also called an ___.", "a": "argument", "hint": "Arg."},
        {"q": f"{L}: Fill - Tree traversal types include in-order, pre-order, and ___.", "a": "post-order", "hint": "After."},
        {"q": f"{L}: Fill - Hash function maps keys to ___.", "a": "buckets", "hint": "Bins."},
        {"q": f"{L}: Fill - A graph without cycles is ___.", "a": "acyclic", "hint": "No cycles."},
        {"q": f"{L}: Fill - BFS uses a ___.", "a": "queue", "hint": "FIFO."},
        {"q": f"{L}: Fill - DFS commonly uses a ___.", "a": "stack", "hint": "LIFO."},
        {"q": f"{L}: Fill - JSON is a ____ format.", "a": "text", "hint": "Human readable."},
        {"q": f"{L}: Fill - HTTP 200 stands for ___.", "a": "OK", "hint": "Success."},
        {"q": f"{L}: Fill - Modulus operator returns the ____.", "a": "remainder", "hint": "Division result."},
        {"q": f"{L}: Fill - Stable sort preserves ____ order.", "a": "relative", "hint": "Equal keys."},
    ]
    return [{"type": "fill", "question": it["q"], "answer": it["a"], "hint": it["hint"]} for it in items]

# Language-specific banks (Easy MCQ)
LANGUAGE_EASY_MCQ = {
    "python": [
        {"question": "Python: Which keyword defines a function?", "options": ["function", "def", "fn", "define"], "correct": 1, "hint": "Three letters."},
        {"question": "Python: Which creates a list?", "options": ["{}", "[]", "()", "<>"], "correct": 1, "hint": "Square brackets."},
        {"question": "Python: Add item to list?", "options": ["add", "append", "push", "insert"], "correct": 1, "hint": "Method on list."},
        {"question": "Python: Dictionary literal uses?", "options": ["[]", "{}", "()", "<>"], "correct": 1, "hint": "Curly braces."},
        {"question": "Python: Equality operator?", "options": ["=", "==", ":=", "==="], "correct": 1, "hint": "Two equals."},
    ],
    "javascript": [
        {"question": "JS: Strict equality operator?", "options": ["==", "===", "=", "!="], "correct": 1, "hint": "Checks type and value."},
        {"question": "JS: Declare block-scoped variable?", "options": ["var", "let", "const", "int"], "correct": 1, "hint": "ES6."},
        {"question": "JS: Array end insertion?", "options": ["append", "push", "add", "insert"], "correct": 1, "hint": "Mutates array."},
        {"question": "JS: Convert JSON string to object?", "options": ["JSON.stringify", "JSON.parse", "parseJSON", "toObject"], "correct": 1, "hint": "Global JSON."},
        {"question": "JS: Function expression with arrow?", "options": ["->", "=>", "=>=", "<>"], "correct": 1, "hint": "Fat arrow."},
    ],
    "java": [
        {"question": "Java: Entry method signature?", "options": ["main()", "public static void main", "start()", "def main"], "correct": 1, "hint": "With String[] args."},
        {"question": "Java: Add to ArrayList?", "options": ["push", "append", "add", "insert"], "correct": 2, "hint": "java.util."},
        {"question": "Java: Immutable string type?", "options": ["char[]", "String", "StringBuilder", "Text"], "correct": 1, "hint": "java.lang."},
        {"question": "Java: Interface keyword?", "options": ["interface", "trait", "protocol", "abstract"], "correct": 0, "hint": "Type contract."},
        {"question": "Java: HashMap get value?", "options": ["get", "find", "lookup", "fetch"], "correct": 0, "hint": "Key lookup."},
    ],
    "c#": [
        {"question": "C#: Which declares a string?", "options": ["string s;", "var s := ''", "let s = ''", "def s"], "correct": 0, "hint": "Static typing."},
        {"question": "C#: Console output?", "options": ["System.out.println", "Console.WriteLine", "print", "echo"], "correct": 1, "hint": "System namespace."},
        {"question": "C#: Null-coalescing operator?", "options": ["?:", "??", "?.", "=>"], "correct": 1, "hint": "Double ?."},
    ],
    "go": [
        {"question": "Go: Print line?", "options": ["fmt.Println", "console.log", "print", "System.out.println"], "correct": 0, "hint": "fmt pkg."},
        {"question": "Go: Short var declare?", "options": ["=:", ":=", "=>", "<-"], "correct": 1, "hint": "Colon equals."},
        {"question": "Go: Append to slice?", "options": ["push", "append", "add", "insert"], "correct": 1, "hint": "Built-in."},
    ],
    "ruby": [
        {"question": "Ruby: Print line?", "options": ["println", "puts", "echo", "printl"], "correct": 1, "hint": "Adds newline."},
        {"question": "Ruby: Array append?", "options": ["push", "append", "add", "insert"], "correct": 0, "hint": "Method on Array."},
        {"question": "Ruby: Hash literal?", "options": ["{}", "[]", "()", "<>"], "correct": 0, "hint": "Curly braces."},
    ],
    "swift": [
        {"question": "Swift: Constant keyword?", "options": ["let", "var", "const", "final"], "correct": 0, "hint": "Immutable."},
        {"question": "Swift: Optional unwrap?", "options": ["?", "!", "??", "=>"], "correct": 1, "hint": "Force unwrap."},
        {"question": "Swift: Print?", "options": ["println", "print", "echo", "write"], "correct": 1, "hint": "Lowercase."},
    ],
    "kotlin": [
        {"question": "Kotlin: Mutable variable?", "options": ["let", "var", "val", "mut"], "correct": 1, "hint": "var/val."},
        {"question": "Kotlin: Null-safe call?", "options": ["?.", "??", "!.", "::"], "correct": 0, "hint": "Safe call."},
        {"question": "Kotlin: Elvis operator?", "options": ["::", "?:", "=>", "??"], "correct": 1, "hint": "Looks like hair."},
    ],
    "rust": [
        {"question": "Rust: Package tool?", "options": ["npm", "cargo", "pip", "maven"], "correct": 1, "hint": "Build/test."},
        {"question": "Rust: Make variable mutable?", "options": ["let mut", "mut let", "var mut", "set mut"], "correct": 0, "hint": "mut after let."},
        {"question": "Rust: Growable string?", "options": ["&str", "String", "str", "Text"], "correct": 1, "hint": "Heap-allocated."},
    ],
    "php": [
        {"question": "PHP: Variables start with?", "options": ["@", "$", "#", "%"], "correct": 1, "hint": "Dollar."},
        {"question": "PHP: Echo output?", "options": ["print", "echo", "println", "write"], "correct": 1, "hint": "Basic output."},
        {"question": "PHP: Array literal?", "options": ["[]", "{}", "()", "<>"], "correct": 0, "hint": "Short syntax."},
    ],
    "r": [
        {"question": "R: Vector combine?", "options": ["vec()", "c()", "array()", "list()"], "correct": 1, "hint": "Concatenate."},
        {"question": "R: Data frame?", "options": ["df()", "data.frame()", "frame()", "table()"], "correct": 1, "hint": "Base function."},
        {"question": "R: Assign operator?", "options": ["<-", "=", ":=", "=>"], "correct": 0, "hint": "Arrow left."},
    ],
    "perl": [
        {"question": "Perl: Scalar prefix?", "options": ["$", "@", "%", "&"], "correct": 0, "hint": "Scalars use $."},
        {"question": "Perl: Array prefix?", "options": ["$", "@", "%", "#"], "correct": 1, "hint": "At sign."},
        {"question": "Perl: Hash prefix?", "options": ["$", "@", "%", "&"], "correct": 2, "hint": "Percent."},
    ],
    "haskell": [
        {"question": "Haskell: Evaluation strategy?", "options": ["strict", "lazy", "eager", "dynamic"], "correct": 1, "hint": "Non-strict."},
        {"question": "Haskell: List concatenation?", "options": ["++", "+", ":", "<>"], "correct": 0, "hint": "Two pluses."},
        {"question": "Haskell: Function arrow?", "options": ["->", "=>", ":", "::"], "correct": 0, "hint": "Single arrow."},
    ],
    "julia": [
        {"question": "Julia: Print with newline?", "options": ["println", "printl", "puts", "echo"], "correct": 0, "hint": "Add n."},
        {"question": "Julia: Indexing starts at?", "options": ["0", "1", "-1", "2"], "correct": 1, "hint": "One-based."},
        {"question": "Julia: Pkg REPL key?", "options": ["?", ";", "]", "!"], "correct": 2, "hint": "] enters Pkg mode."},
    ],
    "html": [
        {"question": "HTML: Root element?", "options": ["<root>", "<html>", "<head>", "<body>"], "correct": 1, "hint": "Top node."},
        {"question": "HTML: Hyperlink tag?", "options": ["<link>", "<a>", "<href>", "<url>"], "correct": 1, "hint": "Anchor."},
        {"question": "HTML: Image attribute for source?", "options": ["href", "src", "source", "link"], "correct": 1, "hint": "src."},
    ],
    "css": [
        {"question": "CSS: Select by id?", "options": [".id", "#id", "id", "*id"], "correct": 1, "hint": "Hash."},
        {"question": "CSS: Flex container?", "options": ["display:flex", "flex:container", "flexbox", "layout:flex"], "correct": 0, "hint": "display value."},
        {"question": "CSS: Center with margin ____", "options": ["auto", "center", "0", "auto 0"], "correct": 0, "hint": "Horizontally."},
    ],
    "sql": [
        {"question": "SQL: Select all columns?", "options": ["SELECT *", "GET ALL", "FETCH *", "READ ALL"], "correct": 0, "hint": "Asterisk."},
        {"question": "SQL: Filter rows clause?", "options": ["WHERE", "HAVING", "GROUP BY", "ORDER BY"], "correct": 0, "hint": "Row predicate."},
        {"question": "SQL: Combine rows from two tables?", "options": ["UNION", "JOIN", "GROUP", "MERGE"], "correct": 1, "hint": "ON condition."},
    ],
    "nosql": [
        {"question": "NoSQL: Document store?", "options": ["MySQL", "MongoDB", "PostgreSQL", "SQLite"], "correct": 1, "hint": "BSON."},
        {"question": "NoSQL: Key-value store?", "options": ["Redis", "Oracle", "MariaDB", "DB2"], "correct": 0, "hint": "In-memory."},
        {"question": "NoSQL: Column family?", "options": ["Cassandra", "Neo4j", "HBase", "InfluxDB"], "correct": 0, "hint": "Wide-column."},
    ],
    "bash": [
        {"question": "Bash: Print text?", "options": ["echo", "print", "puts", "println"], "correct": 0, "hint": "Builtin."},
        {"question": "Bash: Variable prefix?", "options": ["@", "$", "#", "%"], "correct": 1, "hint": "Dollar."},
        {"question": "Bash: Make script executable?", "options": ["chmod +x", "run +x", "exec +x", "grant +x"], "correct": 0, "hint": "chmod."},
    ],
    "powershell": [
        {"question": "PowerShell: List directory?", "options": ["ls", "Get-ChildItem", "dir", "All"], "correct": 3, "hint": "Aliases exist."},
        {"question": "PowerShell: Var prefix?", "options": ["$", "@", "%", "#"], "correct": 0, "hint": "Dollar."},
        {"question": "PowerShell: Pipeline?", "options": ["|", "=>", ":", "->"], "correct": 0, "hint": "Pipe."},
    ],
}

# Language-specific banks (Medium Fill)
LANGUAGE_MEDIUM_FILL = {
    "c#": [
        {"q": "C#: Print line Console.____().", "a": "WriteLine", "hint": "PascalCase."},
        {"q": "C#: Null-coalescing ____.", "a": "??", "hint": "Double ?."},
        {"q": "C#: Generic list ____<T>.", "a": "List", "hint": "Collection."},
    ],
    "go": [
        {"q": "Go: Print line fmt.____", "a": "Println", "hint": "Capital P."},
        {"q": "Go: Short declare ____.", "a": ":=", "hint": "Colon equals."},
        {"q": "Go: Append built-in ____.", "a": "append", "hint": "Slices."},
    ],
    "ruby": [
        {"q": "Ruby: Print newline ____.", "a": "puts", "hint": "Adds newline."},
        {"q": "Ruby: Array append ____.", "a": "push", "hint": "Method."},
        {"q": "Ruby: Hash literal ____.", "a": "{}", "hint": "Curly."},
    ],
    "swift": [
        {"q": "Swift: Immutable keyword ____.", "a": "let", "hint": "Constant."},
        {"q": "Swift: Optional unwrap ____.", "a": "!", "hint": "Force."},
        {"q": "Swift: Safe optional call ____.", "a": "?", "hint": "Chaining."},
    ],
    "kotlin": [
        {"q": "Kotlin: Mutable var ____.", "a": "var", "hint": "Mutable."},
        {"q": "Kotlin: Immutable var ____.", "a": "val", "hint": "Read-only."},
        {"q": "Kotlin: Elvis operator ____.", "a": "?:", "hint": "Hair."},
    ],
    "rust": [
        {"q": "Rust: Package tool ____.", "a": "cargo", "hint": "Build/test."},
        {"q": "Rust: Make var mutable ____.", "a": "mut", "hint": "After let."},
        {"q": "Rust: Borrow operator ____.", "a": "&", "hint": "Reference."},
    ],
    "php": [
        {"q": "PHP: Var prefix ____.", "a": "$", "hint": "Dollar."},
        {"q": "PHP: Output ____.", "a": "echo", "hint": "Print."},
        {"q": "PHP: Concat operator ____.", "a": ".", "hint": "Dot."},
    ],
    "r": [
        {"q": "R: Vector combine ____.", "a": "c", "hint": "Single letter."},
        {"q": "R: Data frame ____.", "a": "data.frame", "hint": "Base."},
        {"q": "R: Assign op ____.", "a": "<-", "hint": "Arrow."},
    ],
    "perl": [
        {"q": "Perl: Scalar prefix ____.", "a": "$", "hint": "Dollar."},
        {"q": "Perl: Array prefix ____.", "a": "@", "hint": "At."},
        {"q": "Perl: Hash prefix ____.", "a": "%", "hint": "Percent."},
    ],
    "haskell": [
        {"q": "Haskell: List concat ____.", "a": "++", "hint": "Two plus."},
        {"q": "Haskell: Lambda starts with ____.", "a": "\\", "hint": "Backslash."},
        {"q": "Haskell: Function arrow ____.", "a": "->", "hint": "Single arrow."},
    ],
    "julia": [
        {"q": "Julia: Print line ____.", "a": "println", "hint": "Adds newline."},
        {"q": "Julia: Indexing starts at ____.", "a": "1", "hint": "One-based."},
        {"q": "Julia: Pkg REPL key ____.", "a": "]", "hint": "Right bracket."},
    ],
    "html": [
        {"q": "HTML: Root element ____.", "a": "html", "hint": "Tag name."},
        {"q": "HTML: Anchor tag ____.", "a": "a", "hint": "Links."},
        {"q": "HTML: Image source attr ____.", "a": "src", "hint": "Attribute."},
    ],
    "css": [
        {"q": "CSS: ID selector prefix ____.", "a": "#", "hint": "Hash."},
        {"q": "CSS: Class selector prefix ____.", "a": ".", "hint": "Dot."},
        {"q": "CSS: Flex display ____.", "a": "flex", "hint": "display:"},
    ],
    "sql": [
        {"q": "SQL: Filter rows clause ____.", "a": "WHERE", "hint": "Row filter."},
        {"q": "SQL: Group aggregation ____.", "a": "GROUP BY", "hint": "Grouping."},
        {"q": "SQL: Sort results ____.", "a": "ORDER BY", "hint": "Sorting."},
    ],
    "nosql": [
        {"q": "NoSQL: Document store ____.", "a": "MongoDB", "hint": "BSON."},
        {"q": "NoSQL: Key-value store ____.", "a": "Redis", "hint": "In-memory."},
        {"q": "NoSQL: Graph db ____.", "a": "Neo4j", "hint": "Nodes/edges."},
    ],
    "bash": [
        {"q": "Bash: Print ____.", "a": "echo", "hint": "Builtin."},
        {"q": "Bash: Var prefix ____.", "a": "$", "hint": "Dollar."},
        {"q": "Bash: Shebang prefix ____.", "a": "#!", "hint": "Interpreter line."},
    ],
    "powershell": [
        {"q": "PowerShell: List dir ____.", "a": "Get-ChildItem", "hint": "Aliases: ls, dir."},
        {"q": "PowerShell: Var prefix ____.", "a": "$", "hint": "Dollar."},
        {"q": "PowerShell: Hashtable literal ____.", "a": "@{}", "hint": "At braces."},
    ],
}

# Dynamic question bank generators per level
def generate_easy_mcq(language: str) -> list:
    norm = _normalize_lang(language)
    # Language-specific overrides
    if norm in LANGUAGE_EASY_MCQ:
        pool = LANGUAGE_EASY_MCQ[norm]
    else:
        # Neutral fallback MCQs (no Python-specific wording)
        pool = [
            {"question": f"{language}: Which operator compares equality?", "options": ["=", "==", ":=", "=>"], "correct": 1, "hint": "Two equals."},
            {"question": f"{language}: Arrays/Lists are typically ____ indexed.", "options": ["0-based", "1-based", "2-based", "-1-based"], "correct": 0, "hint": "Starts at zero in many languages."},
            {"question": f"{language}: Which term means error during execution?", "options": ["syntax error", "runtime error", "compile-time error", "linker error"], "correct": 1, "hint": "Occurs while running."},
            {"question": f"{language}: Which structure stores key-value pairs?", "options": ["array", "map", "stack", "queue"], "correct": 1, "hint": "Associative."},
            {"question": f"{language}: Which loop is best for iterating a count?", "options": ["for", "while", "do-while", "switch"], "correct": 0, "hint": "Counter variable."},
            {"question": f"{language}: Which data type represents true/false?", "options": ["int", "string", "bool", "float"], "correct": 2, "hint": "Logical."},
            {"question": f"{language}: Which operator often concatenates strings?", "options": ["+", "-", "*", "/"], "correct": 0, "hint": "Overloaded in many languages."},
            {"question": f"{language}: What term describes a function inside a class?", "options": ["field", "method", "module", "macro"], "correct": 1, "hint": "Invoked on objects."},
            {"question": f"{language}: Which DS follows FIFO?", "options": ["stack", "queue", "set", "tree"], "correct": 1, "hint": "First-in, first-out."},
            {"question": f"{language}: Which DS follows LIFO?", "options": ["stack", "queue", "set", "tree"], "correct": 0, "hint": "Last-in, first-out."},
            {"question": f"{language}: Sorting ascending typically uses ____ sort built-in.", "options": ["custom", "library", "manual", "random"], "correct": 1, "hint": "Standard library."},
            {"question": f"{language}: Which notation describes time complexity?", "options": ["Sigma", "Theta", "Big-O", "Lambda"], "correct": 2, "hint": "Upper bound."},
        ]
    # Ensure at least 15; repeat-shuffle and trim
    while len(pool) < 15:
        pool = pool + pool
    random.shuffle(pool)
    mcqs = pool[:15]
    # Normalize shape: add type and explanation
    explained = []
    for q in mcqs:
        opts = q.get("options", [])
        ci = q.get("correct", 0)
        correct_text = opts[ci] if 0 <= ci < len(opts) else ""
        default_exp = f"{correct_text} is correct because it directly matches the concept referenced in the question."
        explanation = q.get("explanation") or default_exp
        explained.append({**q, "type": "mcq", "explanation": explanation})
    return explained

def generate_medium_fill(language: str) -> list:
    norm = _normalize_lang(language)
    # Language-specific overrides
    if norm in LANGUAGE_MEDIUM_FILL:
        items = LANGUAGE_MEDIUM_FILL[norm]
        return [{"type": "fill", "question": it["q"], "answer": it["a"], "hint": it["hint"], "explanation": f"The blank should be '{it['a']}' because {it['hint']}"} for it in items]
    # Neutral fallback (no language-specific keywords)
    items = [
        {"q": f"{language}: Fill - First index in zero-based indexing is ___.", "a": "0", "hint": "Not one."},
        {"q": f"{language}: Fill - Structure storing key/value is a ___.", "a": "map", "hint": "Associative."},
        {"q": f"{language}: Fill - LIFO structure is a ___.", "a": "stack", "hint": "Opposite of queue."},
        {"q": f"{language}: Fill - FIFO structure is a ___.", "a": "queue", "hint": "First-in/First-out."},
        {"q": f"{language}: Fill - Equality comparison commonly uses ___.", "a": "==", "hint": "Double equals."},
        {"q": f"{language}: Fill - Algorithm complexity is described with ____ notation.", "a": "Big-O", "hint": "Asymptotic."},
        {"q": f"{language}: Fill - Binary uses base ___.", "a": "2", "hint": "Two symbols."},
        {"q": f"{language}: Fill - A collection without duplicates is a ___.", "a": "set", "hint": "Mathematical term."},
        {"q": f"{language}: Fill - Sorting ascending uses ____ order.", "a": "increasing", "hint": "Opposite of decreasing."},
        {"q": f"{language}: Fill - An error at runtime is a ____ error.", "a": "runtime", "hint": "During execution."},
        {"q": f"{language}: Fill - A function parameter is also called an ___.", "a": "argument", "hint": "Arg."},
        {"q": f"{language}: Fill - Tree traversal types include in-order, pre-order, and ___.", "a": "post-order", "hint": "After."},
        {"q": f"{language}: Fill - Hash function maps keys to ___.", "a": "buckets", "hint": "Bins."},
        {"q": f"{language}: Fill - A graph without cycles is ___.", "a": "acyclic", "hint": "No cycles."},
        {"q": f"{language}: Fill - BFS uses a ___.", "a": "queue", "hint": "FIFO."},
    ]
    return [{"type": "fill", "question": it["q"], "answer": it["a"], "hint": it["hint"], "explanation": f"The correct fill is '{it['a']}' because {it['hint']}"} for it in items]

def _code_question(func_name: str, prompt: str, tests: list, starter: str = "", solution: str = "", explanation: str = ""):
    # Provide solution and detailed explanation for review
    return {"type": "code", "function": func_name, "question": prompt, "tests": tests, "starter": starter, "solution": solution or None, "explanation": explanation or "Solve using basic control flow and data structures."}

def generate_hard_code(language: str) -> list:
    # For non-Python, we still collect answers but cannot execute; we mark as correct if non-empty.
    # For Python, we execute tests against user code defining specific function names.
    q = []
    # Tailor prompt prefix per language for clarity
    prefix = f"[{language}] "
    q.append(_code_question(
        "reverse_string",
        f"{prefix}Write a function reverse_string(s) that returns the reversed string.",
        tests=[{"in": ("abc",), "out": "cba"}, {"in": ("",), "out": ""}, {"in": ("racecar",), "out": "racecar"}],
        starter="",
        solution="def reverse_string(s):\n\treturn s[::-1]",
        explanation="Strings support slicing. s[::-1] creates a reversed copy in O(n) time by stepping with -1."
    ))
    q.append(_code_question(
        "factorial",
        f"{prefix}Write factorial(n) that returns n! for n>=0.",
        tests=[{"in": (0,), "out": 1}, {"in": (3,), "out": 6}, {"in": (5,), "out": 120}],
        starter="",
        solution="def factorial(n):\n\tif n < 2:\n\t\treturn 1\n\tresult = 1\n\tfor i in range(2, n+1):\n\t\tresult *= i\n\treturn result",
        explanation="Use iterative multiplication from 2..n. Base case 0! and 1! = 1 avoids extra checks."
    ))
    q.append(_code_question(
        "is_palindrome",
        f"{prefix}Write is_palindrome(s) returning True if s reads same forward/backward.",
        tests=[{"in": ("abba",), "out": True}, {"in": ("abc",), "out": False}, {"in": ("a",), "out": True}],
        starter="",
        solution="def is_palindrome(s):\n\treturn s == s[::-1]",
        explanation="A string equals its reverse iff it is a palindrome. Slicing builds the reversed view."
    ))
    q.append(_code_question(
        "fibonacci",
        f"{prefix}Write fibonacci(n) returning nth Fibonacci with fib(0)=0,fib(1)=1.",
        tests=[{"in": (0,), "out": 0}, {"in": (1,), "out": 1}, {"in": (7,), "out": 13}],
        starter="",
        solution="def fibonacci(n):\n\ta, b = 0, 1\n\tfor _ in range(n):\n\t\ta, b = b, a + b\n\treturn a",
        explanation="Iterative pair update runs in O(n) time, O(1) space, avoiding slow recursion."
    ))
    q.append(_code_question(
        "sum_list",
        f"{prefix}Write sum_list(nums) that returns sum of a list of numbers.",
        tests=[{"in": ([1,2,3],), "out": 6}, {"in": ([],), "out": 0}],
        starter="",
        solution="def sum_list(nums):\n\ttotal = 0\n\tfor x in nums:\n\t\ttotal += x\n\treturn total",
        explanation="Accumulate elements with a running total. This is linear in the list length."
    ))
    q.append(_code_question(
        "is_prime",
        f"{prefix}Write is_prime(n) returning True if n is a prime (n>=2).",
        tests=[{"in": (2,), "out": True}, {"in": (9,), "out": False}, {"in": (13,), "out": True}],
        starter="",
        solution="def is_prime(n):\n\tif n < 2:\n\t\treturn False\n\tif n % 2 == 0:\n\t\treturn n == 2\n\td = 3\n\twhile d * d <= n:\n\t\tif n % d == 0:\n\t\t\treturn False\n\t\td += 2\n\treturn True",
        explanation="Check divisibility up to sqrt(n). Skip even divisors for efficiency."
    ))
    q.append(_code_question(
        "count_vowels",
        f"{prefix}Write count_vowels(s) returning the number of vowels aeiou in s.",
        tests=[{"in": ("hello",), "out": 2}, {"in": ("xyz",), "out": 0}],
        starter="",
        solution="def count_vowels(s):\n\tvowels = set('aeiouAEIOU')\n\treturn sum(1 for ch in s if ch in vowels)",
        explanation="Use a set for O(1) membership tests and count matches."
    ))
    q.append(_code_question(
        "unique_elements",
        f"{prefix}Write unique_elements(lst) returning a list of unique elements in order.",
        tests=[{"in": ([1,1,2,3,2],), "out": [1,2,3]}, {"in": ([],), "out": []}],
        starter="",
        solution="def unique_elements(lst):\n\tseen = set()\n\tout = []\n\tfor x in lst:\n\t\tif x not in seen:\n\t\t\tseen.add(x)\n\t\t\tout.append(x)\n\treturn out",
        explanation="Track seen items in a set and append unseen to preserve first occurrence order."
    ))
    q.append(_code_question(
        "sort_numbers",
        f"{prefix}Write sort_numbers(lst) returning a new sorted list ascending.",
        tests=[{"in": ([3,1,2],), "out": [1,2,3]}, {"in": ([],), "out": []}],
        starter="",
        solution="def sort_numbers(lst):\n\treturn sorted(lst)",
        explanation="Use the built-in Timsort which is O(n log n) and stable."
    ))
    q.append(_code_question(
        "square_numbers",
        f"{prefix}Write square_numbers(lst) returning list of squares of numbers.",
        tests=[{"in": ([1,2,3],), "out": [1,4,9]}, {"in": ([],), "out": []}],
        starter="",
        solution="def square_numbers(lst):\n\treturn [x * x for x in lst]",
        explanation="List comprehension maps each element x to x*x in linear time."
    ))
    return q

def get_questions_for_language(language: str, level: str) -> list:
    if level == "Easy":
        return generate_easy_mcq(language)
    if level == "Medium":
        return generate_medium_fill(language)
    if level == "Hard":
        return generate_hard_code(language)
    # Fallback
    return generate_easy_mcq(language)

def _safe_exec_python(user_code: str, func_name: str, tests: list) -> tuple:
    """Execute user code in restricted env and run tests. Returns (passed, total, error_msg)."""
    allowed_builtins = {
        'range': range, 'len': len, 'sum': sum, 'abs': abs, 'min': min, 'max': max,
        'enumerate': enumerate, 'map': map, 'filter': filter, 'zip': zip, 'all': all, 'any': any,
        'sorted': sorted, 'list': list, 'dict': dict, 'set': set, 'tuple': tuple
    }
    g = {"__builtins__": allowed_builtins}
    l = {}
    try:
        exec(user_code, g, l)
        func = l.get(func_name) or g.get(func_name)
        if not callable(func):
            return (0, len(tests), f"Function {func_name} not found.")
        passed = 0
        for t in tests:
            args = t.get("in", ())
            expected = t.get("out")
            try:
                result = func(*args)
            except Exception as e:
                return (passed, len(tests), f"Runtime error: {e}")
            if result == expected:
                passed += 1
        return (passed, len(tests), None)
    except Exception as e:
        return (0, len(tests), f"Execution error: {e}")

# Expected question counts per level
LEVEL_COUNTS = {"Easy": 15, "Medium": 15, "Hard": 10}

# Initialize session state
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = None
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'current_level' not in st.session_state:
    st.session_state.current_level = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level_scores' not in st.session_state:
    st.session_state.level_scores = {}
if 'badges' not in st.session_state:
    st.session_state.badges = {}
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'prev_questions_seen' not in st.session_state:
    # Tracks used question texts per key "<norm_lang>:<level>"
    st.session_state.prev_questions_seen = {}
if 'awaiting_start' not in st.session_state:
    st.session_state.awaiting_start = False
if 'saved_code' not in st.session_state:
    st.session_state.saved_code = {}
if 'level_questions' not in st.session_state:
    # Stores the concrete question sets used per level
    st.session_state.level_questions = {}
if 'answers' not in st.session_state:
    # Stores user's answer per level per index: {"<level>": {idx: value}}
    st.session_state.answers = {}
if 'marked' not in st.session_state:
    # Stores marked for review flags: {"<level>": set(indices)}
    st.session_state.marked = {}
if 'registered' not in st.session_state:
    st.session_state.registered = False
if 'registration' not in st.session_state:
    st.session_state.registration = {}
if 'captcha_code' not in st.session_state:
    st.session_state.captcha_code = None
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False
if 'exam_feedback' not in st.session_state:
    st.session_state.exam_feedback = {"rating": None, "comments": ""}
if 'view_scorecard' not in st.session_state:
    st.session_state.view_scorecard = False
if 'registrations' not in st.session_state:
    # Map of full_name(lowercased) -> registration dict
    st.session_state.registrations = {}
if 'tests_counted' not in st.session_state:
    st.session_state.tests_counted = False
if 'attempt_recorded' not in st.session_state:
    st.session_state.attempt_recorded = False

# Persistence helpers for registrations
_REG_FILE = os.path.join(os.path.dirname(__file__), 'registrations.json')

def _load_registrations_from_disk():
    try:
        if os.path.exists(_REG_FILE):
            with open(_REG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    st.session_state.registrations = data
    except Exception:
        pass

def _save_registrations_to_disk():
    try:
        with open(_REG_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.registrations, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _generate_captcha():
    """Generate a random 5-character alphanumeric CAPTCHA and store it in session."""
    charset = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(charset) for _ in range(5))
    st.session_state.captcha_code = code
    return code

def make_questions(language: str, level: str) -> list:
    """Create a randomized, language-tailored question set for the level."""
    # Build full pool from generator and top-up with neutral items by level
    full_pool = get_questions_for_language(language, level)
    if level == "Easy":
        full_pool = full_pool + [{**q, "type": "mcq"} for q in _neutral_easy_mcq(language)]
    elif level == "Medium":
        full_pool = full_pool + _neutral_medium_fill(language)
    # Deduplicate by question text
    seen_q = set()
    pool = []
    for q in full_pool:
        qt = q.get("question", "")
        if qt not in seen_q:
            seen_q.add(qt)
            pool.append(q)
    random.shuffle(pool)
    target = LEVEL_COUNTS.get(level, len(pool))
    # Exclude previously used questions for this language+level
    norm = _normalize_lang(language)
    key = f"{norm}:{level}"
    prev = set(st.session_state.prev_questions_seen.get(key, []))
    fresh = [q for q in pool if q.get("question", "") not in prev]
    selection = []
    for q in fresh:
        if len(selection) >= target:
            break
        selection.append(q)
    if len(selection) < target:
        # Fill remaining from the rest of pool (even if previously seen) without duplicates in this selection
        for q in pool:
            if len(selection) >= target:
                break
            if q not in selection:
                selection.append(q)
    # Update history (cap memory to last 100 entries per key)
    used_texts = [q.get("question", "") for q in selection]
    updated = list(prev)
    updated.extend([t for t in used_texts if t not in prev])
    st.session_state.prev_questions_seen[key] = updated[-100:]
    return selection

def reset_quiz():
    """Reset the quiz to initial state"""
    st.session_state.selected_language = None
    st.session_state.current_level = None
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.level_scores = {}
    st.session_state.badges = {}
    st.session_state.show_hint = False
    st.session_state.quiz_completed = False
    st.session_state.questions = None
    st.session_state.awaiting_start = False
    st.session_state.saved_code = {}
    st.session_state.level_questions = {}

def calculate_badge(score, total_questions):
    """Calculate badge based on score percentage with new thresholds."""
    percentage = (score / total_questions) * 100 if total_questions else 0
    if percentage >= 85:
        return "🥇 Gold Badge (Excellent)"
    elif percentage >= 75:
        return "🥈 Silver Badge (Good)"
    elif percentage >= 60:
        return "🥉 Bronze Badge (Keep Improving)"
    else:
        return "❌ No Badge"

def calculate_final_badge(level_scores: dict) -> tuple:
    """Compute average percentage across all three levels and return (avg_percent, badge)."""
    if not level_scores:
        return (0.0, "❌ No Badge")
    total_correct = 0
    total_questions = 0
    for level, score in level_scores.items():
        level_total = LEVEL_COUNTS.get(level, 0)
        total_correct += score
        total_questions += level_total
    avg_percent = (total_correct / total_questions) * 100 if total_questions else 0
    if avg_percent >= 85:
        badge = "🥇 Gold Badge (Excellent)"
    elif avg_percent >= 75:
        badge = "🥈 Silver Badge (Good)"
    elif avg_percent >= 60:
        badge = "🥉 Bronze Badge (Keep Improving)"
    else:
        badge = "❌ No Badge"
    return (avg_percent, badge)

def get_final_message():
    """Determine final message based on average badge across all levels."""
    avg_percent, final_badge = calculate_final_badge(st.session_state.level_scores)
    if 'Gold' in final_badge:
        return "🎉🏆 Congratulations! You're ready for the mock interview! 🎉🏆"
    elif 'Silver' in final_badge:
        return "👍😊 You're ready, but you have to practice some more. 👍😊"
    elif 'Bronze' in final_badge:
        return "😔📚 You're not eligible for mock interview. Keep studying! 😔📚"
    else:
        return "😞📚 Keep practicing to improve your average score. 😞📚"

# Main app layout
st.title("💻 Programming Quiz Challenge")
st.markdown("Test your programming skills and earn badges!")

# Registration gate
if not st.session_state.registered:
    # Load registrations from disk so returning users can lookup
    if not st.session_state.registrations:
        _load_registrations_from_disk()
    st.header("Exam Registration Form")

    # Ensure a CAPTCHA exists on first load
    if not st.session_state.captcha_code:
        _generate_captcha()

    # Fast path for users already registered
    st.subheader("Already registered?")
    with st.form("lookup_form", clear_on_submit=False):
        lookup_name = st.text_input("Enter your registered full name")
        lookup_submit = st.form_submit_button("Continue")
    if lookup_submit:
        key = (lookup_name or "").strip().lower()
        if not st.session_state.registrations:
            _load_registrations_from_disk()
        reg = st.session_state.registrations.get(key)
        if reg:
            st.session_state.registration = reg
            st.session_state.registered = True
            st.success(f"Welcome back, {reg.get('full_name','Candidate')}!")
            st.rerun()
        else:
            st.error("You are not registered. Please fill the form below.")

    with st.form("registration_form", clear_on_submit=False):
        role = st.selectbox("You are", ["Student", "Staff"]) 
        full_name = st.text_input("Full name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"]) 
        email = st.text_input("Email ID")
        mobile = st.text_input("Mobile number")
        course = st.text_input("Registered course")

        # CAPTCHA display with refresh inside form (separate submit button)
        cap_col1, cap_col2 = st.columns([3, 1])
        with cap_col1:
            st.markdown(f"**CAPTCHA:** `{st.session_state.captcha_code}`")
        with cap_col2:
            refresh_clicked = st.form_submit_button("🔄 Refresh CAPTCHA", type="secondary")

        captcha_input = st.text_input("Enter CAPTCHA code (case-insensitive)")

        submitted = st.form_submit_button("Register and Continue", type="primary")

    # Handle refresh within the form
    if refresh_clicked:
        _generate_captcha()
        st.info("CAPTCHA refreshed.")

    # Handle registration submit
    if submitted:
        errors = []
        if not full_name.strip():
            errors.append("Full name is required")
        if not email.strip() or ("@" not in email or "." not in email.split("@")[-1]):
            errors.append("Valid email is required")
        if not mobile.strip().isdigit() or len(mobile.strip()) < 10:
            errors.append("Valid mobile number (10+ digits) is required")
        if not course.strip():
            errors.append("Registered course is required")

        cap_ok = isinstance(captcha_input, str) and captcha_input.strip().upper() == (st.session_state.captcha_code or "").upper()
        if not cap_ok:
            errors.append("CAPTCHA not Matched")

        # Regenerate CAPTCHA after each attempt
        _generate_captcha()

        if errors:
            for e in errors:
                st.error(e)
            if cap_ok:
                st.success("CAPTCHA Matched")
            else:
                st.error("CAPTCHA not Matched")
        else:
            st.success("CAPTCHA Matched")
            st.session_state.registration = {
                "role": role,
                "full_name": full_name.strip(),
                "gender": gender,
                "email": email.strip(),
                "mobile": mobile.strip(),
                "course": course.strip(),
                "tests_taken": 0,
            }
            # Save to registrations index for future lookups
            st.session_state.registrations[full_name.strip().lower()] = dict(st.session_state.registration)
            _save_registrations_to_disk()
            st.session_state.registered = True
            st.success("Registration successful. Proceed to choose a category.")
            st.rerun()
    st.stop()

# Category and language selection
if st.session_state.selected_language is None:
    # Step 1: Pick a category
    if st.session_state.selected_category is None:
        # Welcome banner
        if st.session_state.registration.get("full_name"):
            st.markdown(f"### Welcome {st.session_state.registration.get('full_name')}!")
        st.header("Choose a Category")
        cat_names = list(CATEGORY_TO_LANGUAGES.keys())
        for row_start in range(0, len(cat_names), 2):
            cols = st.columns(2)
            for i in range(2):
                idx = row_start + i
                if idx < len(cat_names):
                    with cols[i]:
                        if st.button(cat_names[idx], use_container_width=True, type="primary"):
                            st.session_state.selected_category = cat_names[idx]
                            st.rerun()
    else:
        # Step 2: Pick a language within the chosen category
        st.header(f"{st.session_state.selected_category} - Select a Language")
        langs = CATEGORY_TO_LANGUAGES.get(st.session_state.selected_category, [])
        for row_start in range(0, len(langs), 3):
            cols = st.columns(3)
            for i in range(3):
                idx = row_start + i
                if idx < len(langs):
                    lang = langs[idx]
                    with cols[i]:
                        if st.button(lang, use_container_width=True):
                            st.session_state.selected_language = lang
                            st.rerun()
        st.divider()
        if st.button("⬅️ Back to Categories", type="secondary"):
            st.session_state.selected_category = None
            st.rerun()

# Level selection
elif st.session_state.current_level is None:
    st.header(f"Choose Difficulty Level - {st.session_state.selected_language}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Easy", use_container_width=True, type="primary"):
            st.session_state.current_level = "Easy"
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.questions = make_questions(st.session_state.selected_language, "Easy")
            st.session_state.level_questions['Easy'] = list(st.session_state.questions)
            st.session_state.awaiting_start = True
            st.session_state.answers['Easy'] = {}
            st.session_state.marked['Easy'] = set()
            st.rerun()
    
    with col2:
        if st.button("🟡 Medium", use_container_width=True, type="primary"):
            st.session_state.current_level = "Medium"
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.questions = make_questions(st.session_state.selected_language, "Medium")
            st.session_state.level_questions['Medium'] = list(st.session_state.questions)
            st.session_state.awaiting_start = True
            st.session_state.answers['Medium'] = {}
            st.session_state.marked['Medium'] = set()
            st.rerun()
    
    with col3:
        if st.button("🔴 Hard", use_container_width=True, type="primary"):
            st.session_state.current_level = "Hard"
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.questions = make_questions(st.session_state.selected_language, "Hard")
            st.session_state.level_questions['Hard'] = list(st.session_state.questions)
            st.session_state.awaiting_start = True
            st.session_state.answers['Hard'] = {}
            st.session_state.marked['Hard'] = set()
            st.rerun()
    
    if st.button("🔄 Change Language", type="secondary"):
        reset_quiz()
        st.rerun()

# Quiz interface
elif not st.session_state.quiz_completed:
    language = st.session_state.selected_language
    level = st.session_state.current_level
    # Pre-test instructions gate
    if st.session_state.awaiting_start:
        total = LEVEL_COUNTS.get(level, 0)
        st.header(f"{level} Instructions")
        st.markdown(f"You will attempt {total} questions in the {level} level for {language}.")
        if level == "Easy":
            st.markdown("""
            - Multiple Choice Questions (MCQs)
            - Use Previous/Next to navigate, Mark for Review to revisit
            - Submit Level at the end to finalize answers
            """)
        elif level == "Medium":
            st.markdown("""
            - Fill-in-the-blank questions
            - Use Previous/Next to navigate, Mark for Review to revisit
            - Submit Level at the end to finalize answers
            """)
        else:  # Hard
            st.markdown("""
            - Coding questions
            - Controls: Save (persist), Run (check), Submit (finalize current)
            - Use Previous/Next to navigate, Mark for Review to revisit
            - Submit Level at the end to finalize answers
            """)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Take Test", type="primary"):
                st.session_state.awaiting_start = False
                st.rerun()
        with c2:
            if st.button("⬅️ Back", type="secondary"):
                st.session_state.current_level = None
                st.session_state.awaiting_start = False
                st.session_state.questions = None
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.rerun()
        st.stop()
    # Use stored randomized set; generate if missing (e.g., on first render)
    if not st.session_state.questions:
        st.session_state.questions = make_questions(language, level)
    questions = st.session_state.questions
    current_q = st.session_state.current_question
    
    if current_q < len(questions):
        question_data = questions[current_q]
        qtype = question_data.get("type", "mcq")
        
        # Progress bar
        progress = (current_q + 1) / len(questions)
        st.progress(progress)
        st.caption(f"Question {current_q + 1} of {len(questions)}")
        
        # Question
        st.header(f"Question {current_q + 1}")
        st.subheader(question_data.get("question", ""))
        
        # Hint button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💡 Hint", type="secondary", key=f"hint_{current_q}"):
                st.session_state.show_hint = True
        if st.session_state.show_hint and question_data.get("hint"):
            st.info(f"💡 **Hint:** {question_data['hint']}")

        answered_correctly = False
        show_submit = True

        if qtype == "mcq":
            # Multiple choice
            selected_option = st.radio(
                "Choose your answer:",
                question_data["options"],
                key=f"mcq_{current_q}"
            )
            # Save answer to session
            st.session_state.answers[level][current_q] = selected_option

        elif qtype == "fill":
            # Fill in the blanks
            user_text = st.text_input("Type your answer:", key=f"fill_{current_q}")
            st.session_state.answers[level][current_q] = user_text

        elif qtype == "code":
            # Coding question with Save, Run, and Submit controls
            starter = question_data.get("starter", "")
            code_key = f"{language}:{level}:q{current_q}"
            saved = st.session_state.saved_code.get(code_key, starter)
            user_code = st.text_area("Write your solution:", value=saved, height=240, key=f"code_{current_q}")
            col_a, col_b, col_c = st.columns([1,1,1])
            with col_a:
                if st.button("💾 Save", key=f"save_{current_q}"):
                    st.session_state.saved_code[code_key] = user_code
                    st.success("Saved")
            with col_b:
                if st.button("▶️ Run", key=f"run_{current_q}"):
                    if "python" in language.lower():
                        func_name = question_data.get("function")
                        tests = question_data.get("tests", [])
                        passed, total, err = _safe_exec_python(user_code, func_name, tests)
                        if err:
                            st.error(err)
                        st.info(f"Tests passed: {passed}/{total}")
                    else:
                        # For all non-Python languages, accept any non-empty code and simulate run
                        if not user_code.strip():
                            st.warning("Please provide some code before running (simulation).")
                        else:
                            st.info("Run simulated for non-Python languages. Your code looks submitted.")
            with col_c:
                if st.button("✅ Submit", type="primary", key=f"submit_{current_q}"):
                    # Evaluate on submit
                    if "python" in language.lower():
                        func_name = question_data.get("function")
                        tests = question_data.get("tests", [])
                        passed, total, err = _safe_exec_python(user_code, func_name, tests)
                        if err:
                            st.error(err)
                        st.info(f"Tests passed: {passed}/{total}")
                        if err is None and passed == total:
                            answered_correctly = True
                    else:
                        # For non-Python languages, mark correct if any code is provided
                        if user_code.strip():
                            answered_correctly = True

                    # Persist last code
                    st.session_state.saved_code[code_key] = user_code
                    # Save code as answer
                    st.session_state.answers[level][current_q] = user_code

        else:
            st.warning("Unknown question type. Skipping...")
            
        # Navigation and actions
        nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns(5)
        with nav_c1:
            if st.button("⬅️ Previous", disabled=current_q == 0):
                st.session_state.current_question = max(0, current_q - 1)
                st.session_state.show_hint = False
                st.rerun()
        with nav_c2:
            if st.button("➡️ Next", disabled=current_q >= len(questions) - 1):
                st.session_state.current_question = min(len(questions) - 1, current_q + 1)
                st.session_state.show_hint = False
                st.rerun()
        with nav_c3:
            if st.button("🔖 Mark for Review"):
                st.session_state.marked[level].add(current_q)
                st.info("Marked for review")
        with nav_c4:
            if st.button("⬅️ Back to Levels"):
                st.session_state.current_level = None
                st.session_state.questions = None
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.rerun()
        with nav_c5:
            if st.button("✅ Submit Level", type="primary"):
                # Grade all answers for this level
                total_score = 0
                for idx, q in enumerate(questions):
                    qtype2 = q.get("type", "mcq")
                    ans = st.session_state.answers[level].get(idx)
                    if qtype2 == "mcq":
                        if ans is None:
                            continue
                        correct = q["options"][q["correct"]]
                        if ans == correct:
                            total_score += 1
                    elif qtype2 == "fill":
                        expected = str(q.get("answer", "")).strip().lower()
                        if isinstance(ans, str) and ans.strip().lower() == expected:
                            total_score += 1
                    elif qtype2 == "code":
                        if "python" in language.lower():
                            func_name = q.get("function")
                            tests = q.get("tests", [])
                            code_key2 = f"{language}:{level}:q{idx}"
                            code_text = st.session_state.saved_code.get(code_key2, ans or "")
                            if code_text.strip():
                                passed, total, err = _safe_exec_python(code_text, func_name, tests)
                                if err is None and passed == total:
                                    total_score += 1
                        else:
                            # For all non-Python languages, accept any non-empty code either saved or as answer
                            code_key2 = f"{language}:{level}:q{idx}"
                            code_text = st.session_state.saved_code.get(code_key2, ans or "")
                            if isinstance(code_text, str) and code_text.strip():
                                total_score += 1
                st.session_state.score = total_score
                st.session_state.current_question = len(questions)
                st.session_state.show_hint = False
                st.rerun()
    
    else:
        # Level completed
        total_questions = len(questions)
        badge = calculate_badge(st.session_state.score, total_questions)
        st.session_state.level_scores[level] = st.session_state.score
        st.session_state.badges[level] = badge
        
        st.header("🎯 Level Completed!")
        st.subheader(f"Your Score: {st.session_state.score}/{total_questions}")
        st.subheader(f"Badge Earned: {badge}")
        
        # Show all completed levels
        if len(st.session_state.level_scores) > 1:
            st.subheader(" All Levels Summary")
            for completed_level, score in st.session_state.level_scores.items():
                level_questions = LEVEL_COUNTS.get(completed_level, 0)
                level_badge = st.session_state.badges[completed_level]
                st.write(f"**{completed_level}:** {score}/{level_questions} - {level_badge}")
        
        # Check if all levels completed
        if len(st.session_state.level_scores) == 3:
            st.session_state.quiz_completed = True
            st.rerun()
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Continue to Next Level", type="primary"):
                    st.session_state.current_level = None
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.questions = None
                    st.rerun()
            
            with col2:
                if st.button("🔄 Start Over", type="secondary"):
                    reset_quiz()
                    st.rerun()

# Final results
else:
    # Record attempt and maintain history
    reg = st.session_state.registration or {}
    key = (reg.get("full_name", "").strip().lower())
    if st.session_state.quiz_completed and not st.session_state.attempt_recorded and key:
        if not st.session_state.registrations:
            _load_registrations_from_disk()
        entry = st.session_state.registrations.get(key) or dict(reg)
        if not isinstance(entry.get("tests_history"), list):
            entry["tests_history"] = []
        # Build attempt record
        level_scores = dict(st.session_state.level_scores)
        total_questions = sum(LEVEL_COUNTS.get(lvl, 0) for lvl in level_scores.keys())
        total_correct = sum(level_scores.values())
        avg_percent = (total_correct / total_questions) * 100 if total_questions else 0.0
        attempt = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "category": st.session_state.selected_category,
            "language": st.session_state.selected_language,
            "level_scores": level_scores,
            "average_percent": avg_percent,
        }
        entry["tests_history"].append(attempt)
        entry["tests_taken"] = len(entry["tests_history"])
        st.session_state.registrations[key] = entry
        st.session_state.registration["tests_taken"] = entry["tests_taken"]
        st.session_state.registration["tests_history"] = entry["tests_history"]
        _save_registrations_to_disk()
        st.session_state.attempt_recorded = True

    st.header("🏆 Quiz Complete!")
    
    # Show all results
    st.subheader("📊 Final Results")
    for level, score in st.session_state.level_scores.items():
        level_questions = LEVEL_COUNTS.get(level, 0)
        level_badge = st.session_state.badges[level]
        st.write(f"**{level}:** {score}/{level_questions} - {level_badge}")
    
    # Final average and message
    avg_percent, final_badge = calculate_final_badge(st.session_state.level_scores)
    st.subheader("📊 Average Across Levels")
    st.write(f"Average: {avg_percent:.1f}% - {final_badge}")

    st.subheader("🎯 Final Assessment")
    final_message = get_final_message()
    st.markdown(f"### {final_message}")

    # Post-exam feedback section
    st.subheader("📝 Exam Feedback")
    if not st.session_state.feedback_submitted:
        with st.form("feedback_form", clear_on_submit=False):
            rating = st.select_slider("Rate your exam experience", options=[1,2,3,4,5], value=4)
            comments = st.text_area("Any feedback or suggestions?", value="")
            fb_submit = st.form_submit_button("Submit Feedback", type="primary")
        if fb_submit:
            st.session_state.exam_feedback = {"rating": rating, "comments": comments}
            st.session_state.feedback_submitted = True
            st.success("Thank you! Your feedback has been recorded.")
    else:
        st.info(f"Thanks for your feedback! Rating: {st.session_state.exam_feedback.get('rating')}/5")
        if st.session_state.exam_feedback.get('comments'):
            st.caption("Your comments:")
            st.write(st.session_state.exam_feedback.get('comments'))

    # Solutions & Explanations
    st.subheader("📘 Solutions & Explanations")
    for lvl_name, qs in st.session_state.level_questions.items():
        with st.expander(f"{lvl_name} - Review"):
            for idx, q in enumerate(qs, start=1):
                qtype = q.get("type", "mcq")
                st.markdown(f"**Q{idx}.** {q.get('question','')}")
                if qtype == "mcq":
                    opts = q.get("options", [])
                    correct_idx = q.get("correct", 0)
                    if 0 <= correct_idx < len(opts):
                        st.write(f"Correct Answer: {opts[correct_idx]}")
                    if q.get("explanation"):
                        st.caption(f"Explanation: {q['explanation']}")
                elif qtype == "fill":
                    st.write(f"Expected: {q.get('answer','')}")
                    if q.get("explanation"):
                        st.caption(f"Explanation: {q['explanation']}")
                elif qtype == "code":
                    st.caption("Tests were used to validate your solution.")
                    # If a solution/explanation exists, show it
                    if q.get("solution"):
                        st.code(q.get("solution"), language="python")
                    if q.get("explanation"):
                        st.write(q.get("explanation"))
    
    # Action buttons row
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("⬅️ Back to Categories"):
            st.session_state.selected_category = None
            st.session_state.selected_language = None
            st.session_state.current_level = None
            st.rerun()
    with a2:
        if st.button("🔄 Take Quiz Again", type="primary"):
            reset_quiz()
            st.rerun()
    with a3:
        # Prefer opening the dedicated Score Card page if available
        try:
            st.page_link("pages/Score_Card.py", label="📄 Open Score Card Page")
        except Exception:
            if st.button("📄 View Score Card"):
                st.session_state.view_scorecard = True
                st.rerun()
    # Additional page links
    try:
        st.page_link("pages/Leaderboard.py", label="🏅 Open Leaderboard")
    except Exception:
        pass

    if st.session_state.view_scorecard:
        st.divider()
        st.header("🎓 Score Card")
        reg = st.session_state.registration or {}
        full_name = reg.get("full_name", "Candidate")
        st.markdown(f"**Name:** {full_name}")
        history = reg.get("tests_history", [])
        if history:
            current = history[-1]
            attempt_no = len(history)
            st.markdown(f"**Attempt:** #{attempt_no}")
            st.markdown(f"**Category:** {current.get('category','-')}")
            st.markdown(f"**Language:** {current.get('language','-')}")
            st.subheader("Levels and Scores")
            for lvl in ["Easy", "Medium", "Hard"]:
                if lvl in current.get("level_scores", {}):
                    sc = current["level_scores"][lvl]
                    tq = LEVEL_COUNTS.get(lvl, 0)
                    st.markdown(f"- **{lvl}**: {sc}/{tq}")
            st.markdown(f"**Average:** {current.get('average_percent',0):.1f}%")

            # Previous attempt summary
            if attempt_no > 1:
                prev = history[-2]
                st.subheader("Previous Attempt Summary")
                st.markdown(f"- **Attempt:** #{attempt_no-1}")
                st.markdown(f"- **Category:** {prev.get('category','-')}")
                st.markdown(f"- **Language:** {prev.get('language','-')}")
                st.markdown(f"- **Average:** {prev.get('average_percent',0):.1f}%")

            # Scores over attempts bar chart
            st.subheader("Progress Over Attempts")
            scores = [a.get("average_percent", 0) for a in history]
            st.bar_chart(scores)
        else:
            st.info("No attempts found.")

# Sidebar with instructions
with st.sidebar:
    st.header(" Instructions")
    st.markdown("""
    1. **Choose Language**: Select the category you belong to in programming languages
    2. **Pick Difficulty**: Easy, Medium, or Hard
    3. **Answer Questions**: Multiple choice with hints available
    4. **Earn Badges** (per level): 
       - Badge 1: 85%+ (Excellent)
       - Badge 2: 75-84% (Medium)
       - Badge 3: 60-74% (Poor)
    5. **Complete All Levels**: Take all three difficulty levels
    """)
    
    st.header(" Badge System")
    st.markdown("""
    - **Per Level**: B1 ≥ 85%, B2 75–84%, B3 60–74%
    - **Final Badge**: Average across all levels using the same thresholds
    """)
    
    if st.session_state.selected_language:
        st.header(f"Current: {st.session_state.selected_language}")
        if st.session_state.current_level:
            st.write(f"Level: {st.session_state.current_level}")
        if st.session_state.level_scores:
            st.write("Completed Levels:")
            for level, score in st.session_state.level_scores.items():
                st.write(f"- {level}: {score} points")