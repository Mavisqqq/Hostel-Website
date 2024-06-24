from hostel.models import Block


def single_well_info(request):
    blocks = Block.objects.all()
    k = 0
    for block in blocks:
        if request.user in block.user.all():
            k += 1
            return {'in_block': 1, 'block_slug': block.slug}
    if k == 0:
        return {'in_block': 0}
