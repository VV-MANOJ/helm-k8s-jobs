{{/*
Expand the name of the chart.
*/}}
{{- define "kubernetes-job-chart.name" -}}
{{- .Chart.Name | lower -}}
{{- end -}}

{{/*
Generate the job name from the chart name and job name.
*/}}
{{- define "kubernetes-job-chart.jobName" -}}
{{- .Values.name | cat "-" .Release.Name | lower -}}
{{- end -}}

