import perfectmeal as pm

##
## Test food/meal adding/subtracting capabilities
##

## first test without JSON involved


def test_add_subtract_1():
    type_list = ['elements', 'vitamins', 'energy', 'sugars', 'amino_acids',
                     'other', 'composition']

    food_one = pm.Food(type_list)
    for _type in type_list:
        for subtype in food_one.__dict__[_type]:
            food_one.__dict__[_type][subtype] = 10

    food_two = pm.Food(type_list)
    for _type in type_list:
        for subtype in food_two.__dict__[_type]:
            food_two.__dict__[_type][subtype] = 8

    food_three = pm.Food(type_list)
    for _type in type_list:
        for subtype in food_three.__dict__[_type]:
            food_three.__dict__[_type][subtype] = 5.555
            

    meal_one = pm.Meal(type_list)
    meal_one.add(food_one)
    meal_one.add(food_two)
    meal_one.add(food_three)
    meal_one.subtract(food_one)
    meal_one.subtract(food_two)
    meal_one.subtract(food_three)

    errors = {}
    for _type in type_list:
        for subtype in food_one.__dict__[_type]:
            if meal_one.__dict__[_type][subtype] != 0:
                errors[_type+'__'+subtype] = meal_one.__dict__[_type][subtype]

    return errors

def test_add_subtract_2():
    ## add then subtract one food, then add and subtract another food
    type_list = ['elements', 'vitamins', 'energy', 'sugars', 'amino_acids',
                     'other', 'composition']
    food_one = pm.get_food("Kale, scotch, raw")
    food_two = pm.get_food("Kale, raw")
    meal_one = pm.Meal(type_list)
    meal_one.add(food_one)
    meal_one.subtract(food_one)
    meal_one.add(food_two)
    meal_one.subtract(food_two)
    
    errors = {}
    for _type in type_list:
        for subtype in food_one.__dict__[_type]:
            print 'type, subtype:', _type, subtype
            if meal_one.__dict__[_type][subtype] != 0:
                errors[_type+'__'+subtype] = meal_one.__dict__[_type][subtype]
    return errors
    ## currently passing

def test_add_subtract_3():
    ## add two foods, then subtract both (recreates a known problem showing up in
    ## the GUI layer) **** Problem found, rounding error, now any number close
    ## enough to zero afrer subtraction is rounded to zero
    type_list = ['elements', 'vitamins', 'energy', 'sugars', 'amino_acids',
                     'other', 'composition']
    food_one = pm.get_food("Kale, scotch, raw")
    food_two = pm.get_food("Kale, raw")
    meal_one = pm.Meal(type_list)
    meal_one.add(food_one)
    meal_one.add(food_two)
    meal_one.subtract(food_one)
    meal_one.subtract(food_two)
    
    errors = {}
    for _type in type_list:
        for subtype in food_one.__dict__[_type]:
            if meal_one.__dict__[_type][subtype] != 0 and\
               meal_one.__dict__[_type][subtype] != None:
                errors[_type+'__'+subtype] = meal_one.__dict__[_type][subtype]
    return errors
    


            
