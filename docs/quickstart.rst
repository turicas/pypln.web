===============
Getting Started
===============


For this quick start guide we will use our demonstration instalation located at
http://demo.pypln.org . You may use it to test PyPLN, but be aware that any data
you upload there will possibly be available to other users and that data will
be periodically deleted.


To start using PyPLN you need to create an user account. Just click the
`Register <http://demo.pypln.org/accounts/register/>`_ link on the top menu.
During this tutorial we will use the user `demo` (the password is also `demo`).


PyPLN provides a `RESTful API <https://en.wikipedia.org/wiki/Representational_state_transfer>`
that allows you to create corpora, upload documents and get the results of your
analysis. You can browse this API in a simple way just by visiting the website
with a browser. But we can use the API programatically to automate our
process. This allows us to handle larger data sets in much less time and with
less chance of a manual error getting in our way.


In this quickstart guide we will write some `Python <http://www.python.org>`
code to create a corpus, upload every PDF file in a specific directory to PyPLN
and download the plain text extracted from the PDF. For that you'll need
`requests <http://docs.python-requests.org/en/latest/>` which makes writing code
to interact with an HTTP service very easy. You can install it by running `pip
install requests` or following the provided `installation instructions <http://docs.python-requests.org/en/latest/user/install/#install>`


So let's start. First, we need to create a new corpus:

.. code-block:: python

    import requests

    response = requests.post('http://demo.pypln.org/corpora/',
        data={'name': 'pdfs', 'description': 'My PDFs'}, auth=('demo', 'demo'))


`response` should have a 201 (created) status code, and contain corpus
information:

>>> response.status_code
201
>>> response.json()
{u'created_at': u'1979-01-01T00:00:01.000Z',
 u'description': u'My PDFs',
 u'documents': [],
 u'name': u'pdfs',
 u'owner': u'demo',
 u'url': u'http://demo.pypln.org/corpora/1/'}

.. note::
    A user cannot have two corpora with the same name. If you're getting a 400
    (Bad Request) reply when trying to reproduce this step, please check if the
    user doesn't already have a corpus with the same name you're trying to
    create.

Please note that the corpus information will definetly change when you run
this code (the creation date will be different, so will the url and probably
other data). If you have similar output, this means your corpus was created
successfully. Now you can upload your files to this corpus. Let's do this for
all the pdf files in a directory called `pdfs`:

.. code-block:: python

    import glob

    # We'll just keep our credentials here just to make it easier to use
    credentials = ('demo', 'demo')

    # The corpus url comes from the last response
    corpus_url = response.json()['url']
    data = {'corpus': corpus_url}

    for filename in glob.glob('pdfs/*.pdf'):
        print('Sending {}...'.format(filename))
        with open(filename, 'r') as fp:
            files = {'blob': fp}
            resp = requests.post('http://demo.pypln.org/documents/', data=data,
                files=files, auth=credentials)
            print(resp.status_code)

This should print the message `'Sending <filename>...'` followed by a `'201'` for
each file you have in your `pdfs` directory. If this happened, it means the
upload was successfull.

After receiving the documents, PyPLN will process them, and extract the text
from each PDF. This can take a while.

We can get information on all documents, by running:

.. code-block:: python

    documents_response = requests.get('http://demo.pypln.org/documents/', auth=credentials)

`response` here will have a list of all the documents you have. So you can, for
example, get the plain text extracted from them:

.. code-block:: python

    for document in documents_response.json():
        # we need to get the document's base property url
        properties_url = document['properties']
        plain_text_url = properties_url + 'text'
        doc_text_info = requests.get(plain_text_url, auth=credentials)
        doc_text = doc_text_info.json()['value']
        # Let's just print the length of the text, otherwise we could have a
        # lot of output.
        print(len(doc_text))


This should print the length of the text extracted from each of your PDFs. You
can see all the available properties for each document in the `properties` url
provided in it's information (what we called `properties_url` in the code
above).

You can get a list of all properties for each document in the url provided by
'properties':

.. code-block:: python

    # Let's pick one document and work with it
    document = documents_response.json()[0]
    properties_response = requests.get(document['properties'],
            auth=credentials)
    print(properties_response.json()['properties'])

You should see something like this:

.. code-block:: python

        [
            "http://demo.pypln.org/documents/1/properties/mimetype/",
            "http://demo.pypln.org/documents/1/properties/freqdist/",
            "http://demo.pypln.org/documents/1/properties/average_sentence_repertoire/",
            "http://demo.pypln.org/documents/1/properties/language/",
            "http://demo.pypln.org/documents/1/properties/momentum_4/",
            "http://demo.pypln.org/documents/1/properties/average_sentence_length/",
            "http://demo.pypln.org/documents/1/properties/momentum_1/",
            "http://demo.pypln.org/documents/1/properties/pos/",
            "http://demo.pypln.org/documents/1/properties/momentum_3/",
            "http://demo.pypln.org/documents/1/properties/file_metadata/",
            "http://demo.pypln.org/documents/1/properties/tokens/",
            "http://demo.pypln.org/documents/1/properties/repertoire/",
            "http://demo.pypln.org/documents/1/properties/text/",
            "http://demo.pypln.org/documents/1/properties/tagset/",
            "http://demo.pypln.org/documents/1/properties/sentences/",
            "http://demo.pypln.org/documents/1/properties/momentum_2/",
            "http://demo.pypln.org/documents/1/properties/named_entities/"
        ]


.. note::
    Again, the exact result will depend on the document you have uploaded, and
    whether all analysis are finished when you listed the properties.

So if you want, for example, the frequency of tokens in the analysed text, just
get it from the provided url:

.. code-block:: python

    freqdist_response = requests.get("http://demo.pypln.org/documents/1/properties/freqdist/",
            auth=credentials)

    print(freqdist_response.json()['value'])

And you should see a list containing pairs of tokens and it's number of
occurrences in the document.

.. add link to the documentation of the endpoints
