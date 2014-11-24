class EssayFeature():
    """
    Essay feature prototype
    """
    def __init__(self,fun):
        self.fun = fun
    
    def generate(self,essay):
        return self.fun(essay)


class FunctionalTextEssayFeature(EssayFeature):
    """
    Essay functional feature
    It lets you define a single feature based on a passed function
    """
    
    def __init__(self,feature_name,fun):
        self.feature_name = feature_name
        self.fun = fun
        
    def generate(self,essay):
        return {self.feature_name:self.fun(essay)}
        
        
class EssayTextConversion():
    def __init__(self,source,dest,fun):
        self.source = source
        self.dest = dest
        self.fun = fun
        
    def apply(self,essay):
        essay.texts[self.dest] = self.fun(essay.texts[self.source])
        
        
class EssayTextConversionBatch():
    def __init__(self,source,dest,fun):
        self.source = source
        self.dest = dest
        self.fun = fun
        
    def fit(self,essays):
        pass
        
    def apply(self,essay):
        pass


"""
    vector = step.generate(self.essay_name)
                feature_name = step.feature_name
                for essay,value in zip(self.essays, vector):
                    essay.add_features({feature_name:value})
"""
    
class EssayAddVector():
    def __init__(self,feature_name,vector_generate_f):
        self.feature_name = feature_name
        self.vector_generate_f = vector_generate_f
        
    def generate(self,essay_name):
        return self.vector_generate_f(essay_name)
    