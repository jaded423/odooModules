{
    "name": "Global Search",
    "summary": "Google-style global search across multiple models from one search box.",
    "version": "17.0.1.0.0",
    "author": "jaded",
    "website": "",
    "category": "Tools",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "global_search/static/src/js/global_search.js",
            "global_search/static/src/css/global_search.css",
            "global_search/static/src/xml/global_search.xml",
        ],
    },
    "installable": True,
    "application": False,
}
