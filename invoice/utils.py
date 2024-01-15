from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# 
def paginateInvoice(request, results, invoices):
    page = request.GET.get('page')
    results = results
    paginator = Paginator(invoices, results)

    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        invoices = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        invoices = paginator.page(page)

    # 
    leftIndex = (int(page) -4)
    if leftIndex < 1:
        leftIndex = 1

    # 
    rightIndex = (int(page) +5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, invoices