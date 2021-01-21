SPEC = \
    {
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
                        "description": "Gray-scale segmentation mask of shape "
                                       "(h,w)",
                        "type": "ndarray/uint8//",
                        "category": {
                            "name": "segmentation",
                            "labels": ["background", "bright pixels"]
                        }
                    },
                    {
                        "name": "#bright_pixels",
                        "description": "Number of bright pixels",
                        "type": "numeric/int",
                        "category": {
                            "name": "measurement"
                        }
                    }
                ],
                "test_cases": [
                    ["image.png", 130, 'mask_130.png', 8865],
                    ["image.png", 150, 'mask_150.png', 3593],
                    ["image.png", 0, 'mask_0.png', 108204],
                    ["image.png", 255, 'mask_255.png', 0],
                ]
            },
        },
        "module": {
            "author": "Stefan Maetschke",
            "author_email": "stefan.maetschke@gmail.com",
            "description": "Segments bright pixels.",
            "name": "Bright Pixel Segmenter",
            "url": "git@github.com:maet3608/analytics-module-template.git",
            "version": "1.0.0",
            "dependencies": ["mmacommon>=1.3.5"]
        }
    }
