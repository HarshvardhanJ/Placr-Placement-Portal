<template>
  <div v-if="show" class="modal d-block" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content border-0 shadow rounded-4 overflow-hidden">
        <div class="modal-header border-0 pb-0">
          <div>
            <h5 class="modal-title mb-1">Company Details</h5>
            <small class="text-secondary"
              >Profile snapshot for the selected company</small
            >
          </div>

          <button class="btn-close" @click="emit('close')" />
        </div>

        <div class="modal-body pt-4">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Company Name</label
              >
              <div class="fw-medium">{{ display(company?.name) }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Industry</label
              >
              <div class="fw-medium">{{ display(company?.industry) }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Location</label
              >
              <div class="fw-medium">{{ display(company?.location) }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Contact</label
              >
              <div class="fw-medium">{{ display(company?.contact) }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Website</label
              >
              <div class="fw-medium text-truncate">
                {{ display(company?.website) }}
              </div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Status</label
              >
              <div class="fw-medium">{{ display(company?.status) }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Total Drives</label
              >
              <div class="fw-medium">{{ company?.drives ?? 0 }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary small text-uppercase fw-semibold"
                >Created At</label
              >
              <div class="fw-medium">{{ formatDate(company?.created_at) }}</div>
            </div>
          </div>
        </div>

        <div class="modal-footer border-0 pt-0">
          <button class="btn btn-outline-secondary" @click="emit('close')">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="show" class="modal-backdrop fade show" />
</template>

<script setup>
const props = defineProps({
  company: {
    type: Object,
    default: null,
  },
  show: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close"]);

const display = (value) => value || "—";

const formatDate = (value) => {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleDateString([], { dateStyle: "medium" });
};
</script>
