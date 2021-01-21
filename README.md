# Introduction

An **Analytics Module** or short **AModule** is a wrapper around 
analytics code, e.g. a machine learning model, that provides a
standardized but flexible API for running and testing a model.
 
Below a simplified example of a module implementation (located in `module.py`):

```python
class MyCatDetector(Module):

    def __init__(self, *args):
        self.my_model = create_my_model()


    def process(self, image):        
        Module.checktype(self, 'process', 'input', image)
        classid = self.my_model.predict(image)
        Module.checktype(self, 'process', 'output', classid)       
        return classid                    
```

The wrapper class `MyCatDetector` is derived from the base class `Module` and
provides a constructor method `__init__()` that creates a machine learning 
model, and a `process()` method to call the model for some input data.
`Module.checktype()` verifies that model inputs and outputs for the method
`process` are of the correct type, which are defined in `specification.py`.

Every `module.py` is accompanied by a `specification.py` file, that describes
inputs, outputs and other properties of the module. Below a specification 
for the `MyCatDetector` module:

```json
SPEC = \
    {
        "methods": {
            "process": {
                "input": [
                    {
                        "name": "image",
                        "description": "RGB image of shape (h,w,3)",
                        "type": "ndarray/unit8///3"
                    },
                ],
                "output": [
                    {
                        "name": "label",
                        "description": "Predicted class index",
                        "type": "numeric/int",
                    },
                ],
            },
        },
        "module": {
            "author": "Stefan Maetschke",
            "description": "Detects cats in images",
            "name": "My cat detector",
        }
    }
```

The repo `analytics-module-template` contains a template and example code 
that can be used as a starting point when wrapping your analytics code.
Most of the actual functionality of analytics modules is implemented in the
base repo [analytics-module](https://github.quuux.com/aur/analytics-module),
which need to be installed but not modified.

Another requirement is [mma-common](https://github.com/maet3608/mma-common),
which, needs be installed but again requires no modification.


# File overview

Here a quick overview of the important files and folders in the **template**:

**Code**

- `module.py` : Implements the API by wrapping code in a class with 
   specific methods, e.g. `process()`.
   `module.py` typically also contains a main method that provides a
   commandline interface and a pre-defined function `test_module()` for
   regression testing. 
- `specification.py` : Describes inputs, outputs and other properties of
   the module.
- `rest_service.py` : Runs a [Flask](http://flask.pocoo.org/) server to provide 
   a REST service with an API that is automatically derived from 
   `specification.py`. Usually there is no need to touch this code.
   

**Data**

- `resources` : Contains resources such a machine learning models,
   configuration files, or other data files needed to run the module.
- `testdata` : Contains test data for regression testing of the module.
   This data is also used as examples in the GUI provided by the REST service.


**Packages**

- `amod_template` : Contains all code and data needed by the module. 
   Note: Will be renamed when instantiating the template (see below).
- `analytics` : Subpackage under `amod_template` that contains your
   analytics code.


**Other**

These files you usually don't need to touch.

- `setup.py` : Installs the module as Python package under `site-packages`.
- `MANIFEST.in` : Defines which data files are part of the package.
- `.travis.yaml` : Configuration for *Continuous Integration* via Travis.
- `.gitignore` : Tells Git which files to ignore.
- `.gitattributes` Tells Git which files need LFS (large file system).
   Typically these are model weights files greater than 100MB.


# Preparation

Using and implementing an analytics module requires the installation of two
base libraries, `analytics-module` and `mmacommon`. Clone the following repos

```bash
git clone https://github.com/maet3608/mma-common
git clone https://github.quuux.com/aur/analytics-module
```

and then run `setup.py` to install them

```bash
cd mma-common
python setup.py develop

cd ../analytics-module
python setup.py develop
```


# Create an Analytics Module

The following list summarizes the steps required to create an Analytics Module.
More detailed information regarding the implementation of `module.py`
and the required `specification.py` will be provided in the following sections.

1. Create empty git repo for your module, e.g. `my-cat-detector`
2. Download `analytics-module-template` and copy its contents into your repo,  
   e.g. download as zip file using this link: 
   [analytics-module-template.zip](https://github.com/maet3608/analytics-module-template/archive/main.zip)
3. Run `python setup.py init`  
   This will rename `amod_template` to `amod_<working directory>`
   omitting dashes or spaces, e.g. `amod_mycatdetector`
4. Run `python setup.py develop`  
   This will "install" the package under `site-packages`
5. Add your code under `analytics` folder
6. Add weights files under `resources` and test data under `testdata`
7. Implement `process` method in `module.py`
8. Edit `specification.py`


## Folder structure

After Step 1 the folder structure should look like this:

```bash
my-cat-detector
    amod_template
       analytics
       resources
       testdata
       module.py
       specification.py
       ...    
    setup.py
    ...
```

After Step 2 the folder structure should look like as follows:

```bash
my-cat-detector
    amod_mycatdetector
       analytics
       resources
       testdata
       module.py
       specification.py
       ...    
    setup.py
    ...
```

Note that the package `amod_template` has been renamed to `amod_mycatdetector`. 
If you prefer a package name not based on the name of your repo directory run 
`python setup.py init --name <packagename>`


## Notes

- Download `analytics-module-template` and NOT `analytics-module`!
- Ensure that `.travis.yaml` and other files starting with a '.' are copied 
  since they are 'hidden' files.
- Replace the comments in `module.py` with your own descriptions.
- Replace this `README.md` with a description of your code.
- Remove the example code `bright_pixel_segmentation` and the test images.
- If your repo contains large data > 100MB (e.g. model weights) ensure you have
  [Git LFS](https://help.github.com/articles/installing-git-large-file-storage/#platform-linux) 
  installed and activated for your shell.


# Module implementation

All Analytics Modules have a file `module.py` that provides the standarized API
for running your analytics code. This is achieved by implementing a class
derived from `Module` with a `process()` method. A minimal example 
is shown below that assumes your code is located under the 
`amod_mycatdetector.analytics` and provides the functions
`create_my_model` and `load_my_imagedata`:

```python
import sys
import module  
from amodule.base import Module
from amodule.util import create_analytics
from amod_mycatdetector.analytics import create_my_model, load_my_imagedata


class MyDetector(Module):

    def __init__(self, *args):
        self.my_model = create_my_model()


    def process(self, image):
        Module.checktype(self, 'process', 'input', image)
        probs = self.my_model.predict(image)
        Module.checktype(self, 'process', 'output', probs) 
        return probs  
         
                  
def test_module():  # don't change
    name = sys.modules[__name__]
    analytics = create_analytics(name)
    analytics.test()


def main_module(*argv):
    filepath = argv[1]
    image = load_my_imagedata(filepath)
    detector = MyDetector()    
    probs = detector.process(image)
    print(probs) 
    
if __name__ == "__main__":
    main_module(sys.argv)       
```

Typically you create and/or load your model in the `__init__()` method and
call the model (e.g. for prediction) in the `process()` method.

The `process()` method can take any number and type of parameters,
however, its arguments must match the description in `specification.py`.
For instance, here an excerpt of a matching specification

```json
"process": {
    "input": [
        {
            "name": "image",
            "description": "RGB image of shape (h,w,3)",
            "type": "ndarray/uint8///3"
        },
    ],
    "output": [
        {
            "name": "probabilities",
            "description": "Predicted softmax probailities",
            "type": "[numeric/float]",
            "category": {
                "name": "classification",
                "labels": [ "Cat", "Other" ],
            }  
        },      
    ],
```

In this example the input is single image provided as an Numpy array 
(type is `ndarray/uint8///3`) and the output is a float vector
(type is a list of floats `[numeric/float]`), containing the 
softmax probabilites.
Within the body of the method `Module.checktype` is called to verify the
correct types of inputs and outputs when `process` is called. 

Note that you can add additional methods with arbitrary names to the class 
(or rename `process()`). If there is a corresponding description in 
`specification.py` these methods will be exposed via the Rest API.

The `test_module()` function `module.py` is executed when `pytest module.py` 
is called and performs a regression test by comparing the outputs of the 
`process()` method with the expected outputs given in `specification.py` 
and the  `testdata` folder. Usually there is no need to modify this function.

Typically, `module.py` implements a main function (here `main_module()`) that
allows to run the module from the command line with some parameters. There are
no restriction on what the main function does and it does not need to exist 
at all but is very handy for debugging and the creation of test data. 


## Specification

Here we describe the required specification in `specification.py` in more
detail. The specification is a Python dictionary with key/value pairs 
(similar to a JSON file) that is structured as follows

- methods
  - process 
    - inputs
    - outputs
    - testdata
- module

The *methods* section describes all methods of the wrapper class, e.g. the 
`process` method. For each method, descriptions of the *inputs* and *outputs*
are required. *testdata* are optional.
The *module* section contains information such as version number, author
and other meta-data about the module.


### `module` section

The `module` specification value consists of a list of key/value pairs that 
describe the module.  The keys are as follows:

* `name` - name of the module
* `description` - short description of the module's function
* `version` - version number, e.g. 1.0.0
* `author` - name of author
* `auther_email` - email address of author
* `url` - url of Github repository
* `dependencies` - list of Python packages that the module depends on.
  
Here an example:

```json
"module": {
    "author": "Stefan Maetschke",
    "author_email": "stefanrm@au1.quuux.com",
    "description": "Segments bright pixels.",
    "name": "Bright Pixel Segmenter",
    "url": "https://github.quuux.com/aur/analytics-module-template.git",
    "version": "1.0.0",
    "dependencies": [ "Keras >= 2.0.3", "nutsml >= 1.0.28"]
}
```  
  
### `methods` section

The `methods` section contains the names of the methods in the wrapper class,
e.g. `foo` and `bar`, with descriptions of their inputs and outputs, and
an optional section with test cases: 


```json
"foo": {
    "input": [ ],
    "output": [ ],
    "test_cases": [ ],
    
"bar": {
    "input": [ ],
    "output": [ ],  
```

Any method that is listed in the description and has a corresponding 
implementation in the wrapper class will be exposed as a REST service.
For instance, the definition above will generate the following entry points
when running the REST server locally:
 
```
http://localhost:5000/api/run/foo
http://localhost:5000/api/run/bar
```

#### `input` and `output` sections

The `input` and `output` specification are positional lists that define the 
respective input and output arguments for the methods. These lists can be
empty for methods without inputs or outputs. Otherwise they contain the
argument's `name`, `description` and `type`. For example a method that
takes an input image as Numpy array and returns an integer for the 
predicted class label would be described as follows:

```json
"input": [
    {
        "name": "image",
        "description": "RGB image of shape (h,w,3)",
        "type": "ndarray/uint8///3"
    },
],
"output": [
    {
        "name": "label",
        "description": "Predicted class index",
        "type": "numeric/int",
    },     
]
```  

The `output` section can have an additional `category` section that provides
semantic information useful for displaying results. For instance, if the
output is the result of a classification and returns the label index, the
`category` section will have the name `classification` and contains a
list of string labels corresponding to the class label indices
(or softmax probailities):

```json
"output": [
    {
        "name": "label",
        "description": "Predicted class index",
        "type": "numeric/int",
         "category": {
            "name": "classification",
            "labels": ["Cat", "Other"],
        }          
    },     
]
```

The following category specification are supported:

* `classification` - whole image/input classification
* `segmentation` - pixelwise image segmentation
* `detection` - object detection in image, e.g. bounding box
* `measurement` - some measurement, e.g. detected object diameter
* `transformation` - some data transformation, e.g. image normalization

These categories can have additional parameters. Examples are given below: 

```json
 "category": {
    "name": "classification",
    "labels": ["label1", "label2", "..."],
}          
```

```json
 "category": {
    "name": "segmentation",
    "labels": ["label1", "label2", "..."],
}          
```

```json
 "category": {
    "name": "detection",
    "labels": ["label1", "label2", "..."],
}          
```

```json
 "category": {
    "name": "measurement",
    "unit": "meter",
}       
```

As for the input and output types: Technical details can be found in 
`analytics-module/aurmodule/iotypes.py`. Here some common types:

```
'numeric' : any numeric value, e.g. 1, or 0.5 (int or float)
'numeric/int' : any integer value
'numeric/float' : any floating point value

'text/str' : any string

'ndarray/uint16//' : Numpy array used for gray scale images
'ndarray/uint16///3' : Numpy array used for RGB images
'ndarray/image' : Numpy array used for RGB, RGBA or grayscale images. 
```

As you can see, IO types are defined by strings with a syntax similar to 
mime types. The basic format of an IO type is:
```
'main-type/sub-type/params...'
```
where `sub-type` and `params` are optional. A simple example for an
integer type:
```
'numeric/int'
```
Similarly, there are types for floats, strings and booleans:
```
'numeric/float'
'text/str'
'boolean/bool'
```

Note that the subtype can be omitted:
```
'numeric'
'text'
'boolean'
```
where `'numeric'` permits floats or integers.

Numpy arrays can be specified in detail regarding dtype and shape,
using the following format:
```
'ndarray/dtype/#rows/#cols/...'
```

Here some examples:
```
'ndarray/uint8'      : ndarray with dtype uint8 but any shape
'ndarray/uint16//'   : ndarray with dtype uint16 and two dimensions
                       of arbitrary size
'ndarray/uint8/5/10' : ndarray with dtype uint8 and of shape (5,10)
'ndarray/uint8///3'  : ndarray with dtype uint8 and of shape (*,*,3)
'ndarray/image'      : ndarray with uint8 of shape (h,w) or (h,w,3) 
                       or (h,w,4)
```
Note that shape parameters are separated by `/` but can be ommitted by leaving
the parameter value out. For instance, `'ndarray/uint8/5/10'` specifies a
Numpy array with shape `(5,10)`, while `'ndarray/uint8/5/'` specifies an 
array with 5 rows but an arbitrary number of columns. Numpy representations of
RGB images that are of shape `(*,*,3)` are therefore specified as
`'ndarray/uint8///3'`

Finally there is the type 'annotation' (currently no subtype) that validates
the following data structures:

```
('point', ((x, y), ... ))
('circle', ((x, y, r), ...))
('ellipse', ((x, y, rx, ry, rot), ...))
('rect', ((x, y, w, h), ...))
('polyline', (((x, y), (x, y), ...), ...))
```

All the types listed above can be made list types, simply be wrapping them
in rectangular brackets (`[type]`). For instance,
`'[numeric/int]'` describes a list of integers and `'[ndarray/uint8//]'`
would be a list of 2-dimensional ndarrays with dtype uint8. Here some common 
list types:

```
'[numeric/float]'      : list of floats, e.g. class probabilities.
'[test/str]'           : list of strings, e.g. class labels.
'[ndarray/uint16//]'   : list of gray scale images
'[ndarray/uint8///3]'  : list of RGB images
'[ndarray/image]'      : list of RGB, RBGA or grayscale images
```



#### `test_cases` section

Test cases describe input data and expected outputs for a method. These 
test cases will be evaluated when building the module and can be run via

```bash
pytest module.py
``` 

The `test_cases` value is an array of a positional list of terms that 
provide each of the input and expected output values for the method.  
For input or output files, the value can be the filename relative to the 
`testdata` directory in the module directory structure. In the following
an example for the bright pixel segmentation provided in the template:

```json
"methods": {
	"process": {
		"input": [
			{
				"name": "image",
				"description": "RGB image of shape (h,w,3)",
				"type": "ndarray/uint8///3"
			},
			{
				"name": "threshold",
				"description": "Threshold for bright pixels",
				"type": "numeric/int"
			},
		],
		"output": [
			{
				"name": "mask",
				"description": "Segmentation mask of shape (h,w)",
				"type": "ndarray/uint8//",
				"category": {
				    "name": "segmentation",
				    "labels": [ "background", "foreground" ],
				}
			},
			{
				"name": "#bright_pixels",
				"description": "Number of bright pixels",
				"type": "numeric/int",
				"category": {
				    "name": "measurement",
				    "unit": "count"
				}
			}
		],
		"test_cases": [
			["image.png", 130, "mask_130.png", 8865],
			["image.png", 150, "mask_150.png", 3593],
			["image.png", 0, "mask_0.png", 108204],
			["image.png", 255, "mask_255.png", 0],
		]
	},
},
```

Here input data are image files and thresholds and outputs are mask images
and numbers of segmented pixels.


## Installation

If you want to install your Analytics Module run either

```bash
python setup.py develop 
```

or

```bash
python setup.py install 
```

The former has the advantages that any changes to your code will be 'active'
immediately while the later requires you to rerun `setup.py install` if you
want the Python environment let know about the changes.

# REST API

Each analytics module supports a REST API and several web applications - one to 
run a demo and another to execute the analytics module test cases.

To start the REST API and web application on localhost using the 
default port (5000) run:

```bash
python rest_service.py
```

from the `amod_<module name>` directory

Once the analytics module is installed you can start the REST API by running:

```bash
python -m amod_<module name>.rest_service
```

For details of other command line options (host and port settings) run:

```bash
python rest_service.py --help
```


Once the REST API is running, open your browser and enter 
`http://localhost:5000/api` to show the available REST calls. For instance,
the `analytics-module-template` exposes the following example REST API:

```JSON
{
    "name": "Bright Pixel Segmenter", 
    "api_version": "1.2.0", 
    "specification_url": "http://127.0.0.1:5000/api/spec", 
    "run_url": "http://127.0.0.1:5000/api/run{/method}", 
    "debug_url": "http://127.0.0.1:5000/api/debug", 
    "test_url": "http://127.0.0.1:5000/api/test", 
    "cache_url": "http://127.0.0.1:5000/api/cache"
}
```

- If you append `/spec` to the initial URL you will see the analytics 
   specification which defines the REST API - method name, inputs and outputs. 
      
- If you append `/test` to the initial URL you will access the test web application.  
  This allows you to run and see the results of the analytics test cases.  
  These tests are defined in the analytics package but they should give a view 
  of the types of inputs and outputs from the analytics and their capabilities.
  
- If you append `/debug` to the initial URL you will access the 
   debug web application.  This allows you to provide your own data to the 
   analytics for processing. If you run within a docker container and
   would like to upload a file  you need to use the `docker cp` command 
   to first copy data from disk into the container.  Note that such data is not 
   persistent when the container  is shutdown and restarted.
      
- If you append `/run` to the initial URL you will see an example of how 
  to call the analytics programmatically via the REST API, e.g.
  `"http://127.0.0.1:5000/api/run/process?image=ndarray/uint8///3&threshold=numeric/int"` 

Per default, the REST API is single threaded and therefore handles only one 
request at a time. Adding the `--threaded` argument allows you to run
the server multi-threaded:

```bash
python rest_service.py --threaded
```

Note that this is not sufficient for a production server. See
[Flask deployment](http://flask.pocoo.org/docs/0.12/deploying/#deployment)
on how to scale for production.
  
  
## Sending images and Numpy arrays

The Specification describes the IO types for the Python API of an Analytics
Module. Apart from primitive types such as strings or integers most types 
cannot be transported directly via REST calls and need to be encoded or 
converted - specifically Numpy arrays.

The Analytics Module therefore provides a range of converter functions that
map common Web data types such as image files, or data URLs to Numpy arrays. For
instance, if the REST API request the following Numpy array
 `/api/run/process?image=ndarray/uint8///3`, which describes an RGB image, 
it can be provided as an HTTP URL, a file URL, or data URL. Here some examples:
```
/api/run/process?image=https://www.quuux.com/image.jpg
/api/run/process?image=file:///your/file/image.png
/api/run/process?image=data:image/gif;base64,/9j/4SXNR...
``` 

The format of the input image can be anything the Python PIL package 
supports, which covers most common formats such as JPEG, PNG, TIFF and BMP, 
but not DICOM images!

If the answer to a REST API call results in an image or a Numpy array,
it will be returned as a data URL.
Numpy arrays of shape (h,w), (h,w,3) and (h,w,4) with data type `uint8`
can be interpreted as images (grayscale, RGB, RBGA) and will be encoded 
as PNG image in a data URL with the following header: `data:image/png;base64,...` 

Input Numpy arrays that cannot be interpreted as images, e.g. vectors, 4D scans 
or others can be send as files (`.npy` or `.npz`), URLs or data URLs. 
In the case of data URLs they must be send as base64 encoded `.npy` or `.npz` 
files with the appropriate header (`data:ndarray/npz;base64,`). 
Some examples:

```
/api/run/process?oct=data:ndarray/npy;base64,/9j/4SXNR...
/api/run/process?oct=data:ndarray/npz;base64,JHIHUFD...
/api/run/process?oct=https://www.quuux.com/oct.npy
/api/run/process?oct=https://www.quuux.com/oct.npz
/api/run/process?oct=file:///your/file/oct.npy
/api/run/process?oct=file:///your/file/oct.npz
``` 

Finally, lists of all types described above are supported and are simply 
send as comma separated values, e.g. a list of floating point values required
by `/api/run/process?probs=[numeric/float]`, would be provided as
```
/api/run/process?probs=0.2,0.7,0.1
``` 

This works the same for images or Numpy arrays, e.g. given the following 
specification `/api/run/process?images=[ndarray/uint8//]` for a list of
grayscale images, the data could be provide as URLs
```
/api/run/process?images=https://www.quuux.com/image1.jpg,file:///folder/image2.png,...
``` 
or comma separated data URLs
```
/api/run/process?images=data:image/gif;base64,/9j/4SXNR,data:image/png;base64,/9j/4SXNR,...
```  

## curl - examples

Here some example calls for the REST API using `curl`

### Example - specification

Request the Specification

GET:

`curl "http://127.0.0.1:5000/api/spec"`


### Example - method description

Request description of all methods that can be run.

GET:

`curl "http://127.0.0.1:5000/api/run"`


### Example - list of numbers

A list of numbers as integers and a single integer as threshold.

API: 

`api/run/process?numbers=[numeric/int]&threshold=numeric/int` 

GET:

`curl "http://127.0.0.1:5000/api/run/process?numbers=3,4,5&threshold=2"`

POST:

`curl --data "numbers=3,4,5&threshold=2"  http://127.0.0.1:5000/api/run/process`

POST JSON:

`curl --header "Content-Type: application/json" --request POST --data '{"numbers":[3,4],"threshold":2}' http://127.0.0.1:5000/api/run/process
`

NOTE: Windows requires double quotes around string and escaped quotes in string!

`curl --header "Content-Type: application/json" --request POST --data "{\"numbers\":[3,4],\"threshold\":2}" http://127.0.0.1:5000/api/run/process
`


### Example - single image 

Single 2-dimensional numpy array with a data type `uint8` that can be 
interpreted as an image.

API:

`api/run/process?image=ndarray/uint8//` 

GET:

`curl "http://127.0.0.1:5000/api/run/process?image=https://www.quuux.com/image.jpg"`

`curl "http://127.0.0.1:5000/api/run/process?image=file:///your/file/image.png"`

`curl "http://127.0.0.1:5000/api/run/process?image=data:image/gif;base64,/9j/4SXNR..."`

POST JSON:

`curl --header "Content-Type: application/json" --request POST --data '{"image":"https://www.quuux.com/image.jpg"}' http://127.0.0.1:5000/api/run/process
`

`curl --header "Content-Type: application/json" --request POST --data '{"image":"data:image/gif;base64,/9j/4SXNR..."}' http://127.0.0.1:5000/api/run/process
`

### Example - list of images 

List of RGB images

API:

`api/run/process?images=[ndarray/uint8///3]` 

GET:

`curl "http://127.0.0.1:5000/api/run/process?images=https://www.quuux.com/image1.jpg,https://www.quuux.com/image2.jpg"`

`curl "http://127.0.0.1:5000/api/run/process?images=data:image/gif;base64,/9j/4SXNR...,data:image/gif;base64,JILUH..."`

POST:

`curl --data "images=https://www.quuux.com/image1.jpg,https://www.quuux.com/image2.jpg" http://127.0.0.1:5000/api/run/process`


POST JSON:

`curl --header "Content-Type: application/json" --request POST --data '{"images":["https://www.quuux.com/image.jpg","https://www.quuux.com/image.jpg"]}' http://127.0.0.1:5000/api/run/process
`

### Example - list of OCTs

List of OCT volumes

API:

`api/run/process?octs=[ndarray/uint8///]` 

GET:

`curl "http://127.0.0.1:5000/api/run/process?octs=https://www.quuux.com/oct1.npz,https://www.quuux.com/oct2.npz"`

`curl "http://127.0.0.1:5000/api/run/process?octs=https://www.quuux.com/oct1.npy,https://www.quuux.com/oct2.npy"`

`curl "http://127.0.0.1:5000/api/run/process?octs=data:ndarray/npz;base64,/9j/4SXNR...,data:ndarray/npz;base64,JILUH..."`

POST:

`curl --data "octs=file:///your/file/oct1.npz,file:///your/file/oct2.npz" http://127.0.0.1:5000/api/run/process`


POST JSON:

`curl --header "Content-Type: application/json" --request POST --data '{"octs":["https://www.quuux.com/oct1.npy","https://www.quuux.com/oct2.npz"]}' http://127.0.0.1:5000/api/run/process
`





  




