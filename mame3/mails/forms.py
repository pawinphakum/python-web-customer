from django import forms
from django.core.validators import RegexValidator
from django.core import validators

CAR_TYPE_CHOICES = (
    ('1', 'รย.1'),
    ('2', 'รย.2'),
    ('3', 'รย.3'),
    ('12', 'รย.12'),
    ('10', 'รถสองแถว'),
    ('80', 'รถบรรทุก พรบ.ขนส่ง'),
)

POSTCODE_REGEX = RegexValidator(regex=r'^\d{5}$', message='ต้องเป็นตัวเลข 5 หลัก')
PHONE_REGEX = RegexValidator(regex=r'^0\d{9}$', message='ต้องเป็นตัวเลข 10 หลัก และขึ้นต้นด้วย 0')
CAR_NUMBER_REGEX = RegexValidator(regex=r'^\d+$', message='ต้องเป็นตัวเลข 1-4 หลัก')

class CustomerCarForm(forms.Form):
    name = forms.CharField(label='ชื่อ นามสกุล')
    addr = forms.CharField(label='บ้านเลขที่')
    soi = forms.CharField(label='ซอย', required=False)
    road = forms.CharField(label='ถนน', required=False)
    moo = forms.CharField(label='หมู่', required=False)
    tumbon = forms.CharField(label='ตำบล', initial='ขุนทะเล')
    amphur = forms.CharField(label='อำเภอ', initial='ลานสกา')
    province = forms.CharField(label='จังหวัด', initial='นครศรีธรรมราช')
    postcode = forms.CharField(label='รหัสไปรษณีย์',
        initial='80230',
        validators=[POSTCODE_REGEX],
        widget=forms.TextInput(attrs={'maxlength':5}))
    tel = forms.CharField(label='เบอร์โทรศัพท์',
        validators=[PHONE_REGEX],
        widget=forms.TextInput(attrs={'maxlength':10}),
        help_text='รูปแบบ 0891231234, หรือเว้นว่างไว้',
        required=False)
    remark = forms.CharField(label='หมายเหตุ', required=False)
    car_alphabet = forms.CharField(label='หมวดอักษร', widget=forms.TextInput(attrs={'size':6,'maxlength':3}))
    car_number = forms.CharField(label='เลขทะเบียน',
        validators=[CAR_NUMBER_REGEX],
        widget=forms.TextInput(attrs={'size':6,'maxlength':4}))
    car_province = forms.CharField(label='จังหวัด', initial='นศ', widget=forms.TextInput(attrs={'size':6,'maxlength':2}))
    car_type = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=CAR_TYPE_CHOICES,
        label='ประเภทรถ',
    )
    is_tro = forms.BooleanField(label='ตรวจสภาพ', required=False, initial=True)
    is_insure = forms.BooleanField(label='พ.ร.บ.', required=False, initial=True)
    is_paytax = forms.BooleanField(label='ต่อทะเบียน', required=False, initial=True)
    is_special = forms.BooleanField(label='รายการพิเศษ', required=False)
    is_sms = forms.BooleanField(label='ส่ง SMS', required=False, initial=True, disabled=True)
    expire_date = forms.DateField(label='วันสิ้นอายภาษี',
        input_formats=['%d%m%y'],
        help_text='รูปแบบ ววดดปป, เช่น 250161')


class SearchForm(forms.Form):
    search = forms.CharField(label='ค้นหา', help_text='เลขทะเบียน เช่น 246 , ชื่อลูกค้า เช่น สุชาติ , วันที่สร้าง เช่น 251061')

class SmsForm(forms.Form):
    month = forms.CharField(label='เดือน')
    year = forms.CharField(label='ปี')
