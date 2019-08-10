from time import sleep



def line_0(kwargs):  
    sleep(0.2)
    if kwargs['var'] == 0:  
        if kwargs['endres'] != 1:  
            kwargs['endres'] = 2    
    
    else: 	
        kwargs['endres'] = 1  
    kwargs['a'] = kwargs['GLOBAL_b']
    line_0(kwargs)
    return kwargs
    