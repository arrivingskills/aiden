# List with 10 empty lists embedded
main_list = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
]

# Alternative ways to create the same structure:

# Method 1: Using list comprehension
main_list_comprehension = [[] for _ in range(10)]

# Method 2: Using multiplication (note: this creates references to the same list!)
# main_list_multiply = [[]] * 10  # DON'T use this - all sublists reference the same object

# Method 3: Using a loop
main_list_loop = []
for i in range(10):
    main_list_loop.append([])

# Verify the structure
print(f"Main list has {len(main_list)} elements")
print(f"Each element is an empty list: {all(isinstance(item, list) and len(item) == 0 for item in main_list)}")

# Example usage - adding items to individual sublists
main_list[0].append("First item in first sublist")
main_list[1].extend([1, 2, 3])
main_list[2] = ["replaced", "the", "empty", "list"]

print("\nAfter modifications:")
for i, sublist in enumerate(main_list):
    print(f"List {i}: {sublist}")
