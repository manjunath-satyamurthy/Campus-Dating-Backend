from django.db.models import CharField, IntegerField, Model, \
    ImageField, BooleanField, FloatField, AutoField


class AppUser(Model):
    user_Id = CharField(max_length=50, unique=True, blank=False, primary_key=True)
    password = CharField(max_length=50, blank=False)
    firstname = CharField(max_length=25)
    lastname = CharField(max_length=25)
    age = IntegerField(blank=True, default=20)
    sex = CharField(max_length=6, default="Male")
    height = FloatField(blank=True, default=5.0)
    body_type = CharField(max_length=10, default="Average")
    from_age = IntegerField(blank=True, default=20)
    to_age = IntegerField(blank=True, default=40)
    partner = CharField(max_length=6, default="Female")
    partner_height = FloatField(blank=True, default=5.0)
    partner_body_type = CharField(max_length=10, default="Average")
    photo = ImageField(blank=True, default='default_profile.png')

    def upload_photo(self, photo):
        self.photo = photo
        self.save()
        return self 

    def update(self, age, sex, height, body_type, from_age, to_age,
        partner, partner_height, partner_body_type):
        self.age = age
        self.sex = sex
        self.height = height
        self.body_type = body_type
        self.from_age = from_age
        self.to_age = to_age
        self.partner = partner
        self.partner_height = partner_height
        self.partner_body_type = partner_body_type

        self.save()
        return self


class Match(Model):
    user_Id = CharField(max_length=50, unique=True, blank=False)
    likes_user = CharField(max_length=50, blank=False)
    match = BooleanField(default=False)

class Message(Model):
    _id = AutoField(primary_key=True)
    _from = CharField(max_length=50, blank=False)
    _to = CharField(max_length=50, blank=False)
    # order = AutoField()