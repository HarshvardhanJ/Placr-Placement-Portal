<template>
  <StudentModulePlaceholder
    title="Placements"
    subtitle="View offers, joining dates, and download confirmations."
    body="This page is scaffolded and ready for the remaining student dashboard features."
    icon="ti-trophy"
    :actions='actions'
  />
</template>

<script setup>
import StudentModulePlaceholder from "@/components/student/StudentModulePlaceholder.vue";

const actions = [
  {
    "to": "/student/profile",
    "label": "Profile"
  },
  {
    "to": "/student/applications",
    "label": "Applications"
  }
];
</script>
