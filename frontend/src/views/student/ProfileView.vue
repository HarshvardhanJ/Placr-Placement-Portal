<template>
  <StudentModulePlaceholder
    title="Profile"
    subtitle="Update education, skills, resume, and experience."
    body="This page is scaffolded and ready for the remaining student dashboard features."
    icon="ti-id-badge-2"
    :actions='actions'
  />
</template>

<script setup>
import StudentModulePlaceholder from "@/components/student/StudentModulePlaceholder.vue";

const actions = [
  {
    "to": "/student/drives",
    "label": "Drives"
  },
  {
    "to": "/student/settings",
    "label": "Settings"
  }
];
</script>
