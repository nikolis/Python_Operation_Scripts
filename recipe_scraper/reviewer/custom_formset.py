from django.forms.models import (
    BaseInlineFormSet,
	inlineformset_factory,
)


class BaseNestedFormset(BaseInlineFormSet):
  
    def is_valid(self):
        result = super(BaseNestedFormset, self).is_valid()


  
    def save(self, commit=True):
        result = super(BaseNestedFormset, self).save(commit=commit)
	for form in self:
	    form.nested.save(commit=commit)
	return result
    
    

