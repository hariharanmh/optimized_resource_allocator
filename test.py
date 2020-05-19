from main import ResourceAllocator
import json

def test():
    test_cases = {
        'Test Case 0': { 'hours': 1, 'capacity': 1150 },
        'Test Case 1': { 'hours': 5, 'capacity': 230 },
        'Test Case 2': { 'hours': 24, 'capacity': 100 },
        'Test Case 3': { 'hours': 12, 'capacity': 1100 },
        'Test Case 4': { 'hours': 0, 'capacity': 0 },
    }

    file_context = ''

    for case_name, case_props in test_cases.items():
        resourceAllocator = ResourceAllocator(
                hours = case_props['hours'], capacity = case_props['capacity']
            )
        
        file_context += '\n\n'+case_name+'\n'
        file_context += '\tInput:\n\t\tCapacity of {} units for {} Hour\n'.format(case_props['capacity'], case_props['hours'])
        file_context += '\tOutput:\n\t\t{}'.format(json.dumps(resourceAllocator.getOptimumResource()))

    print(file_context)

    with open('test_output.txt', 'w') as file:
        file.write(file_context)

test()