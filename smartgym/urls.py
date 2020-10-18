"""smartgym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import ex
import vis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Arduino/reports', ex.report),
    #url(r'^ArduinoTesting/speed', ex.speed),
    url(r'^APP/signup/', ex.signup),
    url(r'^APP/signin/', ex.signin),
    url(r'^APP/starttraining/', ex.startsession),
    url(r'^APP/stoptraining/', ex.endsession),
    url(r'^APP/Visualise/usersession/speed/overview', vis.userspeedoverview),
    url(r'^APP/Visualise/usersession/acc/overview', vis.useraccoverview),
    url(r'^APP/Visualise/usersession/numberofrepeats', vis.getnumberofrepeats),
    url(r'^APP/Visualise/usersession/numberofsets', vis.getnumberofsets),
    url(r'^APP/Visualise/usersession/sessiontime', vis.getnsessiontime),
    url(r'^APP/Visualise/usersession/calories', vis.getcalories),
    url(r'^APP/Visualise/usercurrentsession/numberofrepeats', vis.realtimerepeats),
    url(r'^APP/UserHistory', vis.userhistory),

]
