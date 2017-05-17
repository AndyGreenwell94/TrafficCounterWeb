from django.shortcuts import get_object_or_404, render, HttpResponse, HttpResponseRedirect
from .models import *
from .forms import ZoneForm, TimeTableForm, ZoneOptionForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


class ExtraContext:
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


@login_required
def index(request):
    profile = request.user.profile
    camera_list = profile.company.camera_set.all()
    context = {
        'camera_list': camera_list,
    }
    return render(request, 'counter/index.html', context)


@login_required
def detail(request, camera_id):
    cam = request.user.profile.company.camera_set.get(pk=camera_id)
    zones = request.user.profile.company.zone_set.filter(camera_id=cam.id,
                                                         group_id=request.user.profile.company.id)
    timetable = request.user.profile.company.timetable_set.filter(camera_id=cam.id,
                                                                  group_id=request.user.profile.company.id)
    context = {
        'camera': cam,
        'zones': zones,
        'timet': timetable,
    }
    return render(request, 'counter/camera.html', context)


def timetable_delete(request, camera_id, timetable_id):
    if request.method == 'POST':
        tt = get_object_or_404(TimeTable, id=timetable_id)
        tt.status = 'deleted'
        tt.save()
    return HttpResponseRedirect('/counter/{}/'.format(camera_id))


class ZoneCreate(CreateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'counter/zone_form.html'
    pk_url_kwarg = 'zone_id'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.camera = get_object_or_404(request.user.profile.company.camera_set.all(), pk=self.kwargs.get('camera_id'))
        return super(ZoneCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.user.profile
        form.instance.group = self.user.profile.company
        form.instance.camera = self.camera
        return super(ZoneCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            zone = self.get_context_data()['zone']
            return reverse('zoneUpdate', kwargs={'camera_id': zone.camera.id,
                                                 'zone_id': zone.id})

    def get_context_data(self, **kwargs):
        context = super(ZoneCreate, self).get_context_data(**kwargs)
        context['cam'] = self.camera
        return context


class ZoneUpdate(UpdateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'counter/zone_form.html'
    pk_url_kwarg = 'zone_id'

    def dispatch(self, request, *args, **kwargs):
        self.camera = get_object_or_404(request.user.profile.company.camera_set.all(), pk=self.kwargs.get('camera_id'))
        get_object_or_404(request.user.profile.company.zone_set, pk=self.kwargs.get('zone_id'))
        return super(ZoneUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            zone = self.get_context_data()['zone']
            return reverse('zoneUpdate', kwargs={'camera_id': zone.camera.id,
                                                 'zone_id': zone.id})

    def get_context_data(self, **kwargs):
        context = super(ZoneUpdate, self).get_context_data(**kwargs)
        context['cam'] = self.camera
        return context


class ZoneDelete(DeleteView):
    model = Zone
    template_name = 'counter/zone_delete.html'
    pk_url_kwarg = 'zone_id'
    success_url = reverse_lazy('index')


class ZoneOptionCreate(CreateView):
    model = ZoneOption
    form_class = ZoneOptionForm
    pk_url_kwarg = 'zoneop_id'
    template_name = 'counter/zoneoptions_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user.profile
        self.camera = get_object_or_404(request.user.profile.company.camera_set.all(), pk=self.kwargs.get('camera_id'))
        self.zone = self.camera.zone_set.get(pk=self.kwargs.get('zone_id'))
        return super(ZoneOptionCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.zone = self.zone
        form.instance.user = self.user
        form.instance.group = self.user.company
        return super(ZoneOptionCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            zoneop = self.get_context_data()['zoneoption']
            return reverse('zoneopUpdate', kwargs={'camera_id': zoneop.zone.camera_id,
                                                   'zone_id': zoneop.zone.id,
                                                   'zoneop_id': zoneop.id, })

    def get_context_data(self, **kwargs):
        context = super(ZoneOptionCreate, self).get_context_data(**kwargs)
        context['cam'] = self.camera
        return context


class ZoneOptionsUpdate(UpdateView):
    model = ZoneOption
    form_class = ZoneOptionForm
    pk_url_kwarg = 'zoneop_id'
    template_name = 'counter/zoneoptions_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.camera = get_object_or_404(request.user.profile.company.camera_set.all(), pk=self.kwargs.get('camera_id'))
        zone = get_object_or_404(request.user.profile.company.zone_set.all(), pk=self.kwargs.get('zone_id'))
        get_object_or_404(zone.zoneoption_set.all(), pk=self.kwargs.get('zoneop_id'))
        return super(ZoneOptionsUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            zoneop = self.get_context_data()['zoneoption']
            return reverse('zoneopUpdate', kwargs={'camera_id': zoneop.zone.camera_id,
                                                   'zone_id': zoneop.zone.id,
                                                   'zoneop_id': zoneop.id, })

    def get_context_data(self, **kwargs):
        context = super(ZoneOptionsUpdate, self).get_context_data(**kwargs)
        context['cam'] = self.camera
        return context


class ZoneOptionDelete(DeleteView):
    model = ZoneOption
    pk_url_kwarg = 'zoneop_id'
    template_name = 'counter/zoneop_delete.html'
    success_url = reverse_lazy('index')


class TimeTableCreate(CreateView):
    model = TimeTable
    form_class = TimeTableForm
    template_name = 'counter/timetable.html'
    pk_url_kwarg = 'timetable_id'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.camera = get_object_or_404(request.user.profile.company.camera_set.all(), pk=self.kwargs.get('camera_id'))
        return super(TimeTableCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.camera = self.camera
        form.instance.status = 'waiting'
        form.instance.interval_length = 600
        form.instance.user = self.user.profile
        form.instance.group = self.user.profile.company
        print(form.instance.days)
        if form.instance.days is None:
            form.instance.days = 'NONE'
        return super(TimeTableCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            timetable = self.get_context_data()['timetable']
            return reverse('timetableUpdate', kwargs={'camera_id': timetable.camera.id,
                                                      'timetable_id': timetable.id})

    def zones_as_choices(self):
        zones = []
        for zone in self.user.profile.company.zone_set.filter(camera_id=self.camera.id):
            zos = []
            for zo in zone.zoneoption_set.all():
                zos.append([zo.id, zo.name])
            new_zone = [zone.name, zos]
            zones.append(new_zone)
        return zones

    def get_context_data(self, **kwargs):
        context = super(TimeTableCreate, self).get_context_data(**kwargs)
        context['cam'] = self.camera
        context['form'].fields['options'].choices = self.zones_as_choices()
        return context


class TimeTableUpdate(UpdateView):
    model = TimeTable
    form_class = TimeTableForm
    template_name = 'counter/timetable.html'
    pk_url_kwarg = 'timetable_id'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.camera = get_object_or_404(request.user.profile.company.camera_set.all(), pk=self.kwargs.get('camera_id'))
        get_object_or_404(request.user.profile.company.timetable_set.all(), pk=self.kwargs.get('timetable_id'))
        return super(TimeTableUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            timetable = self.get_context_data()['timetable']
            return reverse('timetableUpdate', kwargs={'camera_id': timetable.camera.id,
                                                      'timetable_id': timetable.id})

    def zones_as_choices(self):
        zones = []
        for zone in self.user.profile.company.zone_set.filter(camera_id=self.camera.id):
            zos = []
            for zo in zone.zoneoption_set.all():
                zos.append([zo.id, zo.name])
            new_zone = [zone.name, zos]
            zones.append(new_zone)
        return zones

    def get_context_data(self, **kwargs):
        context = super(TimeTableUpdate, self).get_context_data(**kwargs)
        context['cam'] = self.camera
        context['form'].fields['options'].choices = self.zones_as_choices()
        return context


@login_required
def result_list(request, camera_id):
    camera = get_object_or_404(request.user.profile.company.camera_set.all(), pk=camera_id)
    res = Results.objects.filter(zone_id_id__in=camera.zone_set.all())
    table = []
    header = []

    for z in res.values_list('zone_id').distinct():
        for d in res.filter(zone_id=z[0]).values_list('direction').distinct():
            header.append(Zone.objects.get(id=z[0]).name+' '+str(d[0]))

    for t in res.values_list('datetime_start').distinct():
        r = []
        for z in res.values_list('zone_id').distinct():
            for d in res.filter(zone_id=z[0]).values_list('direction').distinct():
                try:
                    o = res.filter(datetime_start__date=t[0].date(), datetime_start__hour=t[0].hour, datetime_start__minute=t[0].minute,
                                   zone_id_id=z[0], direction=d[0])[0]
                except Results.DoesNotExist:
                    o = None
                r.append(o)
        table.append([t[0], r])
    context = {
        'cam': camera,
        'header': header,
        'table': table
    }

    return render(request, 'counter/results.html', context)
