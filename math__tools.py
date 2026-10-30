def add(a, b):
    return a + b


def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


# Bonus Challenge
if __name__ == "__main__":
    print("Testing math_tools directly:")
    print("Add:", add(10, 5))
    print("Average:", average([10, 20, 30]))