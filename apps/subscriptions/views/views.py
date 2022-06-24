from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from djstripe.enums import PlanInterval
from djstripe.settings import djstripe_settings

from ..decorators import redirect_subscription_errors, active_subscription_required
from ..helpers import (get_subscription_urls, get_payment_metadata_from_request, get_price_display_with_currency,
    get_stripe_module)
from ..metadata import get_active_products_with_metadata, \
    get_product_and_metadata_for_subscription, ACTIVE_PLAN_INTERVALS, get_active_plan_interval_metadata
from apps.teams.decorators import team_admin_required, login_and_team_required
from ..models import SubscriptionModelBase


@redirect_subscription_errors
@team_admin_required
def subscription(request, team_slug):
    subscription_holder = request.team
    if subscription_holder.has_active_subscription():
        return _view_subscription(request, subscription_holder)
    else:
        return _upgrade_subscription(request, subscription_holder)


def _view_subscription(request, subscription_holder: SubscriptionModelBase):
    """
    Show user's active subscription
    """
    assert subscription_holder.has_active_subscription()
    product_details = get_product_and_metadata_for_subscription(subscription_holder.active_stripe_subscription)
    subscription = subscription_holder.active_stripe_subscription
    if subscription.plan.amount:
        friendly_payment_amount = get_price_display_with_currency(
            subscription.plan.amount * subscription.quantity,
            subscription.plan.currency,
        )
        base_payment_amount = get_price_display_with_currency(
            subscription.plan.amount,
            subscription.plan.currency,
        )
    else:
        # for variable pricing, get the next invoice from stripe and use that
        stripe = get_stripe_module()
        next_invoice = stripe.Invoice.upcoming(
            subscription=subscription.id,
        )
        friendly_payment_amount = get_price_display_with_currency(next_invoice.total / 100., next_invoice.currency)
        base_payment_amount = None

    return render(request, 'subscriptions/view_subscription.html', {
        'active_tab': 'subscription',
        'page_title': _('Subscription | %(team)s') % {'team': request.team},
        'subscription': subscription,
        'subscription_urls': get_subscription_urls(subscription_holder),
        'friendly_payment_amount': friendly_payment_amount,
        'base_payment_amount': base_payment_amount,
        'product': product_details,
    })


def _upgrade_subscription(request, subscription_holder):
    """
    Show subscription upgrade form / options.
    """
    assert not subscription_holder.has_active_subscription()

    active_products = list(get_active_products_with_metadata())
    default_products = [p for p in active_products if p.metadata.is_default]
    default_product = default_products[0] if default_products else active_products[0]

    def _to_dict(product_with_metadata):
        # for now, just serialize the minimum amount of data needed for the front-end
        product_data = {}
        if PlanInterval.year in ACTIVE_PLAN_INTERVALS:
            product_data['annual_plan'] = {
                'stripe_id': product_with_metadata.annual_plan.id,
                'payment_amount': product_with_metadata.get_annual_price_display(),
                'interval': PlanInterval.year,
            }
        if PlanInterval.month in ACTIVE_PLAN_INTERVALS:
            product_data['monthly_plan'] = {
                'stripe_id': product_with_metadata.monthly_plan.id,
                'payment_amount': product_with_metadata.get_monthly_price_display(),
                'interval': PlanInterval.month,
            }
        return product_data

    template_name = 'subscriptions/upgrade_subscription.html'

    return render(request, template_name, {
        'active_tab': 'subscription',
        'stripe_api_key': djstripe_settings.STRIPE_PUBLIC_KEY,
        'default_product': default_product,
        'active_products': active_products,
        'active_products_json': {str(p.stripe_id): _to_dict(p) for p in active_products},
        'active_plan_intervals': get_active_plan_interval_metadata(),
        'default_to_annual': ACTIVE_PLAN_INTERVALS[0] == PlanInterval.year,
        'subscription_urls': get_subscription_urls(subscription_holder),
        'payment_metadata': get_payment_metadata_from_request(request),
    })


@login_and_team_required
def subscription_demo(request, team_slug):
    subscription_holder = request.team
    return render(request, 'subscriptions/demo.html', {
        'active_tab': 'subscription_demo',
        'subscription': subscription_holder.active_stripe_subscription,
        'product': get_product_and_metadata_for_subscription(
            subscription_holder.active_stripe_subscription
        ),
        'subscription_urls': get_subscription_urls(subscription_holder),
        'page_title': _('Subscription Demo | %(team)s') % {'team': request.team},
    })


@login_and_team_required
@active_subscription_required
def subscription_gated_page(request, team_slug):
    return render(request, 'subscriptions/subscription_gated_page.html')
