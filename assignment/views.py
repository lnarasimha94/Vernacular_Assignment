from django.shortcuts import render
from . import views
from django.http import JsonResponse
from django.views import View
import json
from django.utils.decorators import method_decorator
from typing import List, Dict, Callable, Tuple
SlotValidationResult = Tuple[bool, bool, str, Dict]

# Create your views here.
class ValidationApi(View):


    def validate_finite_values_entity(data):
       
        # retrieving data from json request
        invalid_trigger = data.get('invalid_trigger')
        key = data.get('key')
        name = data.get('name')
        reuse = data.get('reuse')
        support_multiple = data.get('support_multiple')
        pick_first = data.get('pick_first')
        supported_values = data.get('supported_values')
        type_ = data.get('type')
        values = data.get('values')
        
        filled = True
        partially_filled = True
        trigger = ''
        parameters = {}

        valueChecks = []
        validatedTerms = []

        #validating
        if len(values) != 0:
            for dict_index in values:
                if(dict_index['value'] in supported_values):
                   valueChecks.append(True)
                   validatedTerms.append(dict_index['value'].upper())

                else:
                    valueChecks.append(False)

        if(len(values) != 0 and  len(values) == valueChecks.count(True)):
            filled = True
        else:
            filled = False

        print(values)
        print(valueChecks)

        if(len(values) != 0 and  len(values) == valueChecks.count(False)):
            partially_filled = True
        else:
            partially_filled = False
       

        if(not filled):
            trigger =invalid_trigger
        else:
            trigger = ''

        if(filled):
            if pick_first:
                parameters['ids_stated'] = validatedTerms[0]  
            elif support_multiple:
                parameters['ids_stated'] = validatedTerms
            

        return_data = {
            'filled': filled,
            'partially_filled': partially_filled,
            'trigger': trigger,
            'parameters':parameters
        }

        return return_data



    def validate_numeric_entity(data):
        
        # retrieving data from json request
        invalid_trigger = data.get('invalid_trigger')
        key = data.get('key')
        name = data.get('name')
        reuse = data.get('reuse')
        pick_first = data.get('pick_first')
        type_ = data.get('type')
        support_multiple = data.get('support_multiple')
        constraint = data.get('constraint')
        var_name = data.get('var_name')
        values = data.get('values')


        filled = True
        partially_filled = True
        trigger = ''
        parameters = {}


        valueChecks = []
        validatedTerms = []

        #validating
        if len(values) != 0:
            for dict_index in values:

                mod_constraint = constraint.replace(var_name,str(dict_index['value']))
                if(eval(mod_constraint)):
                    valueChecks.append(True)
                    validatedTerms.append(dict_index['value'])

                else:
                    valueChecks.append(False)

        if(len(values) != 0 and  len(values) == valueChecks.count(True)):
            filled = True
        else:
            filled = False


        if(len(values) != 0 and  len(values) == valueChecks.count(False)):
            partially_filled = True
        else:
            partially_filled = False

        if(not filled):
            trigger =invalid_trigger


        if(len(validatedTerms) != 0):
            if pick_first:
                parameters[key] = validatedTerms[0]  
            elif support_multiple:
                parameters[key] = validatedTerms
                

        return_data = {
            'filled': filled,
            'partially_filled': partially_filled,
            'trigger': trigger,
            'parameters':parameters
        }

        return return_data

    def post(self, request):

        data = json.loads(request.body.decode("utf-8"))

        validation_parser = data.get('validation_parser')

        if(validation_parser == 'finite_values_entity'):
            return_data = ValidationApi.validate_finite_values_entity(data)
        elif(validation_parser == 'numeric_values_entity'):
            return_data = ValidationApi.validate_numeric_entity(data)

    
        return JsonResponse(return_data, status=200)