#!/usr/bin/env python3
#            ---------------------------------------------------
#                         Optimized Resource Allocator              
#            ---------------------------------------------------
#           This program allocate machines based on given hours and capacity inputs and eventually 
#           displays output as JSON. 

class ResourceAllocator:

    def __init__(self, **kwargs):
        # Regions; type: Dict;
        self.regions = {
            'New York': {
                'Large': 120, 'XLarge': 230, '2XLarge': 450, '4XLarge': 774, '8XLarge': 1400, '10XLarge': 2820,
            },
            'India': {
                'Large': 140, '2XLarge': 413, '4XLarge': 890, '8XLarge': 1300, '10XLarge': 2970,
            },
            'China': {
                'Large': 110, 'XLarge': 200, '4XLarge': 670, '8XLarge': 1180,
            },
        }
        # Machines; type: Dict;
        self.machines = {'Large': 10, 'XLarge': 20, '2XLarge': 40, '4XLarge': 80, '8XLarge': 160, '10XLarge': 320}
        # Hours; type: int;
        self.hours = int(kwargs.get('hours', 0))
        # Capacity; type: int;
        self.capacity = int(kwargs.get('capacity', 0))

    # Function; input: available_machines(dict of machines); output: best_price;
    def getMachines(self, available_machines):
        available_units = sorted(
                [self.machines[machine] for machine in available_machines.keys()], 
                reverse=True
            )

        total_machine_price = []
        for unit in [unit for unit in available_units if unit <= self.capacity]:
            machine_price = {}
            times = (self.capacity//unit)
            remainder = (self.capacity-(times*unit))
            units = [unit for unit in available_units if (remainder-unit)>=0]
            machine = [key for key, val in self.machines.items() if val == unit][0]
            price = available_machines[machine]
            machine_price.update({'('+machine+', '+str(times)+')': [price, times]})
            while len(units) > 0:
                unit = units[0]
                times = (remainder//unit)
                remainder = (remainder- times*unit)  
                units = [unit for unit in units if (remainder-unit)>=0]
                machine = [key for key, val in self.machines.items() if val == unit][0]                 
                price = available_machines[machine]
                machine_price.update({'('+machine+', '+str(times)+')': [price, times] })

            total_machine_price.append(machine_price)

        best_price = []
        for machine_price in total_machine_price:
            temp_machine = ';'.join(machine_price.keys()) 
            temp_price = sum([(price*times) for price, times in machine_price.values()])
            best_price.append([temp_machine, temp_price])

        return sorted(best_price, key=lambda bp: bp[-1])[0]

    # Function; input: hours, capacity; output: True or False;
    def validate(self):
        try:
            if (isinstance(self.hours, int) and isinstance(self.capacity, int)
                and self.hours != 0 and self.capacity != 0):
                if (self.capacity%10 == 0):
                    return True
            else:
                return False
        except:
            return False

    # Function; input: hours, capacity; output: response dict;
    def getOptimumResource(self):
        output = []
        if self.validate():
            for region_name, machines in self.regions.items():        
                    machines = self.getMachines(machines)
                    output.append({
                        'region': region_name,
                        'total_cost': '${}'.format(machines[-1]*self.hours),
                        'machines': [machine for machine in machines[0].split(';')]
                    })
            response = {'Output': output}
        else:
            response = {'Output': 'No data found'}
        return response
            

if __name__ == '__main__':
    import json

    try: 
        hours = input('No of hours the machine is required to run : ')
        capacity = input('No of units are required in multiples of 10 : ')
        resource_allocator = ResourceAllocator(hours = hours, capacity = capacity)
        response = json.dumps(resource_allocator.getOptimumResource())
        print(response)
    except Exception as e:
        print('Invalid Input !', e)
