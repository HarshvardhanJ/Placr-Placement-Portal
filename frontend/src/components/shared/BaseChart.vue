<template>
  <div class="chart-frame" :style="chartStyle">
    <canvas ref="canvasEl" :aria-label="ariaLabel" role="img"></canvas>
  </div>
</template>

<script setup>
import { Chart, registerables } from "chart.js";
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";

Chart.register(...registerables);

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
  data: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    default: () => ({}),
  },
  ariaLabel: {
    type: String,
    default: "Dashboard chart",
  },
  height: {
    type: [Number, String],
    default: 320,
  },
});

const canvasEl = ref(null);
let chart = null;

const chartStyle = computed(() => ({
  "--chart-height":
    typeof props.height === "number" ? `${props.height}px` : props.height,
}));

const renderChart = async () => {
  await nextTick();
  if (!canvasEl.value) return;

  if (chart) {
    chart.destroy();
  }

  chart = new Chart(canvasEl.value, {
    type: props.type,
    data: props.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      ...props.options,
    },
  });
};

onMounted(renderChart);

watch(
  () => [props.type, props.data, props.options],
  renderChart,
  { deep: true },
);

onBeforeUnmount(() => {
  if (chart) {
    chart.destroy();
  }
});
</script>

<style scoped>
.chart-frame {
  position: relative;
  width: 100%;
  height: var(--chart-height);
  min-height: 0;
}

.chart-frame canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
