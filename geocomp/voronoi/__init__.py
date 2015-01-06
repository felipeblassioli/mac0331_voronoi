# -*- coding: utf-8 -*-

DEBUG = False

def log(s):
    if DEBUG:
        print s

import anim

children = ( 
	( 'anim', 'VoronoiProxy', 'Fortune' ),
)

__all__ = map (lambda a: a[0], children)
