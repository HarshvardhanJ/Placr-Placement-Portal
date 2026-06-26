<template>
  <StudentModulePlaceholder
    title="Settings"
    subtitle="Adjust notifications and account preferences."
    body="This page is scaffolded and ready for the remaining student dashboard features."
    icon="ti-settings"
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
    "to": "/student",
    "label": "Dashboard"
  }
];
</script>
