# PayPal python NVP API wrapper class.
# This is a sample to help others get started on working
# with the PayPal NVP API in Python. 
# This is not a complete reference! Be sure to understand
# what this class is doing before you try it on production servers!
# ...use at your own peril.

## see https://www.paypal.com/IntegrationCenter/ic_nvp.html
## and
## https://www.paypal.com/en_US/ebook/PP_NVPAPI_DeveloperGuide/index.html
## for more information.

# by Mike Atlas / LowSingle.com / MassWrestling.com, September 2007
# No License Expressed. Feel free to distribute, modify, 
#  and use in any open or closed source project without credit to the author

# lot's of changed by Bram de Jong, but no fundamental changes to how the
# paypal API works, just cleanups. Also removed the DoDirectPayment method as
# it is not needed for Freesound

# Example usage: ===============
#    paypal = Paypal()
#    pp_token = paypal.set_express_checkout(100)
#    express_token = paypal.get_express_checkout_details(pp_token['token'])
#    url= paypal.get_paypal_forward_url(express_token['token'])
#    HttpResponseRedirect(url) ## django specific http redirect call for payment


import urllib, cgi

class Paypal:
    
    def __init__(self, debug=True):
        # fill these in with the API values
        self.signature = dict(
            user='bram.d_1207238417_biz_api1.gmail.com',
            pwd='1207238426',
            signature='AQJ29zivYyfU5elMDzHjZFrUPlQeAI8APPQNZpJ9VsW1WHADtltnY3zj',
            version='3.0',
        ) 

        self.urls = dict(
            returnurl='http://www.test.com/',
            cancelurl='http://www.test.com/cancelurl',
        )

        self.debug = debug

        if debug:
            self.API_ENDPOINT = 'https://api-3t.sandbox.paypal.com/nvp'
        else:
            self.API_ENDPOINT = 'https://api-3t.paypal.com/nvp'


    def get_paypal_forward_url(self, token):
        if self.debug:
            return 'https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token=' + token
        else:
            return 'https://www.paypal.com/webscr?cmd=_express-checkout&token=' + token

    
    def query(self, parameters, add_urls=True):
        """for a dict of parameters, create the query-string, get the paypal URL and return the parsed dict"""
        params = self.signature.items() + parameters.items()
        
        print parameters

        if add_urls:
            params += self.urls.items()
        
        # encode the urls into a query string
        params_string = urllib.urlencode( params )
        
        # get the response and parse it
        response = cgi.parse_qs(urllib.urlopen(self.API_ENDPOINT, params_string).read())
       
        # the parsed dict has a list for each value, but all Paypal replies are unique
        return dict([(key.lower(), value[0]) for (key,value) in response.items()])


    def set_express_checkout(self, amount):
        """Set up an express checkout"""
        params = dict(
            method="SetExpressCheckout",
            noshipping=1,
            paymentaction='Authorization',
            amt=amount,
            currencycode='EUR',
            email='', # used by paypal to set email for account creation
            desc='Freesound donation of %d euro' % amount, # description of what the person is buying
            custom=amount, # custom field, can be anything you want
            hdrimg='', # url to image for header, recomended to be stored on https server 
        )

        return self.query(params)
    

    def get_express_checkout_details(self, token):
        """Once the user returns to the return url, call this to get the detailsthe user returns to the return url, call this"""
        params = dict(
            method="GetExpressCheckoutDetails",
            token=token,
        )
        
        return self.query(params)
    
    
    def do_express_checkout_payment(self, token, payer_id, amt):
        """do the actual transaction..."""
        params = dict(
            method="DoExpressCheckoutPayment",
            paymentaction='Sale',
            token=token,
            amt=amt,
            currencycode='EUR',
            payerid=payer_id
        )

        return self.query(params)
        
    
    def get_transaction_details(self, tx_id):
        """get all the details of a transaction that has finished"""
        params = dict(
            method="GetTransactionDetails", 
            transactionid=tx_id
        )
        
        return self.query(params, add_urls=False)