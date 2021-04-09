states = ('s1', 's2','s3', 's4','s5')
 
observations = ('r1', 'r2', 'r3', 'r4', 'r5')
 
start_probability = {'s1': 0.2923467537178092, 
's2': 0.07834602829162132, 
's3': 0.1342038447587958, 
's4': 0.3032281465360899, 
's5': 0.19187522669568371}

#start_p
#0.2923467537178092/0.07834602829162132/0.1342038447587958/0.3032281465360899/0.19187522669568371/
 
transition_probability = {
   's1' : {'s1': 0.8769751693002258, 's2':0.060948081264108354, 's3': 0.003386004514672686, 's4': 0.02708803611738149, 's5': 0.03160270880361174},
   's2' : {'s1': 0.05555555555555555, 's2': 0.7129629629629629, 's3': 0.1882716049382716, 's4': 0.043209876543209874, 's5': 0.0},
   's3' : {'s1': 0.023255813953488372, 's2': 0.0755813953488372, 's3': 0.5116279069767442, 's4': 0.36627906976744184, 's5': 0.023255813953488372},
   's4' : {'s1': 0.008342022940563087, 's2': 0.011470281543274244, 's3': 0.009384775808133473, 's4': 0.867570385818561, 's5': 0.1032325338894682},
   's5' : {'s1': 0.08009153318077804, 's2': 0.034324942791762014, 's3': 0.029748283752860413, 's4': 0.08695652173913043, 's5': 0.7688787185354691},
   }
 
# [[0.8769751693002258, 0.060948081264108354, 0.003386004514672686, 0.02708803611738149, 0.03160270880361174], 
# [0.05555555555555555, 0.7129629629629629, 0.1882716049382716, 0.043209876543209874, 0.0], 
# [0.023255813953488372, 0.0755813953488372, 0.5116279069767442, 0.36627906976744184, 0.023255813953488372], 
# [0.008342022940563087, 0.011470281543274244, 0.009384775808133473, 0.867570385818561, 0.1032325338894682], 
# [0.08009153318077804, 0.034324942791762014, 0.029748283752860413, 0.08695652173913043, 0.7688787185354691]]

emission_probability = {
   's1' : {'r1': 0.42431761786600497, 'r2': 0.2692307692307692, 'r3': 0.019851116625310174, 'r4': 0.141439205955335, 'r5': 0.14516129032258066},
   's2' : {'r1': 0.16666666666666666, 'r2': 0.5787037037037037, 'r3': 0.1388888888888889, 'r4': 0.11574074074074074, 'r5': 0.0},
   's3' : {'r1': 0.0, 'r2': 0.2810810810810811, 'r3': 0.2, 'r4': 0.518918918918919, 'r5': 0.0},
   's4' : {'r1': 0.03588516746411483, 'r2': 0.028708133971291867, 'r3': 0.03588516746411483, 'r4': 0.6483253588516746, 'r5': 0.2511961722488038},
   's5' : {'r1': 0.21550094517958412, 'r2': 0.030245746691871456, 'r3': 0.5, 'r4': 0.3780718336483932, 'r5': 0.3761814744801512},
   }

# Hello Packet (1)
# {'DB Description (2)', 'LS Acknowledge (5)', 'LS Request (3)', 'LS Update (4)', 'Hello Packet (1)'}
# 0.2692307692307692/0.14516129032258066/0.019851116625310174/0.141439205955335/0.42431761786600497/

# DB Description (2)
# {'Hello Packet (1)', 'LS Update (4)', 'LS Request (3)', 'DB Description (2)'}
# 0.16666666666666666/0.11574074074074074/0.1388888888888889/0.5787037037037037/

# LS Request (3)
# {'LS Update (4)', 'LS Request (3)', 'DB Description (2)'}
# 0.518918918918919/0.2/0.2810810810810811/

# LS Update (4)
# {'DB Description (2)', 'LS Acknowledge (5)', 'LS Request (3)', 'LS Update (4)', 'Hello Packet (1)'}
# 0.028708133971291867/0.2511961722488038/0.03588516746411483/0.6483253588516746/0.03588516746411483/

# LS Acknowledge (5)
# {'LS Acknowledge (5)', 'LS Update (4)', 'Hello Packet (1)', 'DB Description (2)'}
# 0.3761814744801512/0.3780718336483932/0.21550094517958412/0.030245746691871456/