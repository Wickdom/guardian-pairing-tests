"""
# Staff Hierarchy Problem

## Description

We would like you to write a program for HR to decide who the best employee is in a company to arbitrate disputes
between different members of staff within the company.

Given a list of a company's staff members and their direct managers,
write a program which, when two specific staff members are specified,
returns the name of the first senior staff member shared by both the specified people.

For example,
if Bob manages both Andrea and Adam, and
Brenda manages Aaron and Aisha, and
Chris manages the managers Bob and Brenda,

if you were to enter Adam and Andrea into your function,
it should output Bob, since these staff members are both directly managed by him.

Likewise, if you entered Adam and Aisha, Chris would be returned,
since Chris is the first person up the chain of seniority that both Adam and Aisha share.

Equally, if you were to enter Andrea and Brenda, the program should return Chris.

In the input file, the relationship between a manager and a managee is expressed
one per line, with the managee's name, followed by a space, followed by the manager's name.

In your program, you can assume that
- no two people in the company share the same name, and that
- everyone in the company sits in one hierarchy with just one person at the top.
- You can also assume there are no loops of people managing each other, and
- everyone (except the person at the top) is managed by just one person.

Sample inputs and outputs are provided below. Try to match this output format in your solution.


## Programming Language

We mostly use Python and Swift. If you are comfortable working with either of these languages,
please complete your solution using one of those. If you are more comfortable using another language, feel free to use that.
You won't be penalised for using a different language, but you might be penalised for making basic mistakes because you are unfamiliar with the language.


## Sample Input/Output

You should find a sample staff.input file in the same directory as this file. This matches the staff hierarchy described above.

With this input file, your program should produce the following output:

```
./staff staff.input Adam Andrea
Bob
```

```
./staff staff.input Adam Aisha
Chris
```

```
./staff staff.input Brenda Andrea
Chris
```

"""

