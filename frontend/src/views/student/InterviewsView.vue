<template>
  <StudentModulePlaceholder
    title="Interviews"
    subtitle="See upcoming interview schedules and feedback."
    body="This page is scaffolded and ready for the remaining student dashboard features."
    icon="ti-calendar-event"
    :actions='actions'
  />
</template>

<script setup>
import StudentModulePlaceholder from "@/components/student/StudentModulePlaceholder.vue";

const actions = [
  {
    "to": "/student/applications",
    "label": "Applications"
  },
  {
    "to": "/student/placements",
    "label": "Placements"
  }
];
</script>
