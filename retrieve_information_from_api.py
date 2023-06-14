with open('plant_details.txt', 'r') as f:
    x = (f.read())
    y = (x.split('\n'))
# returns name of plant
    z = y[0]
    name_of_plant = z[12:]

# returns how often to water
    watering_frequency_of_plant = y[1]
    check_for_num = [int(s) for s in watering_frequency_of_plant.split() if s.isdigit()]

    num_days_till_water = (check_for_num[0])












