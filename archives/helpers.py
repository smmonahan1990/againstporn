def choices(model):
    flair_choices = list(model.objects.exclude(flair__isnull=True).values_list('flair',flat=True))
    return sorted([(i, i) for i in set(flair_choices) if flair_choices.count(i) > 1])
