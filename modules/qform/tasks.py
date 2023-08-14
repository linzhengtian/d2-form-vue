from apps.vadmin.system.models import SaveFile, SaveFileRelation
from modules.qform.models import *
from d2Form.celery import app


@app.task
def clean_qform(ids):
    for id in ids:
        form_datas = FormData.objects.filter(form_template__source_form_id=id)
        for relation_id in form_datas.values_list('id', flat=True):
            SaveFileRelation.objects.filter(model_name="formdata", relation_id=relation_id).delete()
            SaveFileRelation.objects.filter(model_name="formtemplate", relation_id=relation_id).delete()
        form_datas.delete()
        FormTemplate.objects.filter(source_form_id=id).delete()
