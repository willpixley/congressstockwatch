from django.db import models
# Choices

CHAMBER_CHOICES = {
        "H": "House of Representatives",
        "S": "Senate"
    }

PARTY_CHOICES = {
    "D": "Democrat",
    "R":"Republican",
    "I": "Independent"
}


# Create your models here.
class CongressMember(models.Model):
    bio_guide_id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=2)
    last_name = models.CharField(max_length=255)
    chamber = models.CharField(max_length=1, choices=CHAMBER_CHOICES)
    party =  models.CharField(max_length=1, choices=PARTY_CHOICES)
    state = models.CharField(max_length=2)
    term = models.IntegerField(default=1)

    @property
    def full_name(self):
        return f'{self.first_name} {self.middle_initial} {self.last_name}'



class Sector(models.Model):
    sector_code = models.CharField(max_length=16, primary_key=True)
    sector_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Committee(models.Model):
    committee_name = models.CharField(max_length=255)
    chamber = models.CharField(max_length=1, choices=CHAMBER_CHOICES)
    committee_members = models.ManyToManyField(CongressMember, through="CommitteeMembership")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, default='00')

## Join table
class CommitteeMembership(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    member = models.ForeignKey(
        CongressMember,
        on_delete=models.CASCADE,
        to_field='bio_guide_id',  # Reference the string-based primary key
        db_column='bio_guide_id',
    )
    role = models.CharField(max_length=100, default='')

## Join table
class CommitteeSector(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)

class Stock(models.Model):
    ticker = models.CharField(max_length=9, primary_key=True)
    name = models.CharField(max_length=255, default=ticker)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

class Trade(models.Model):
    ACTION_CHOICES = {
        "B": "Buy",
        "S": "Sell",
    }
    id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=1, choices=ACTION_CHOICES)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.IntegerField()
    member = models.ForeignKey(
        CongressMember,
        on_delete=models.CASCADE,
        to_field='bio_guide_id',  # Reference the string-based primary key
        db_column='bio_guide_id',
        related_name='trade'
    )
    traded_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flagged = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    price_at_trade = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    current_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    
    




