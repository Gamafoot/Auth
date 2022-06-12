from flask import render_template, flash
from Modules.Functions import isLogged
from Blueprints.home import bp_home

#============================================================================
#========================== Flask decotartors ===============================
#============================================================================


#============================================================================
#=========================== Custom functions ===============================
#============================================================================


#============================================================================
#========================== Route functions =================================
#============================================================================
@bp_home.route('/')
@isLogged
def home():
    return 'Home'