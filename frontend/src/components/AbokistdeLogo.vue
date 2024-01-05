<template>
  <div :style="style">
    <img
      alt="Abokistde Logo"
      style="height: 100%; width: auto"
      src="~assets/logo.svg"
    />
    <div :style="fontStyle">abokist.de</div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  height?: number;
}

const props = withDefaults(defineProps<Props>(), {
  height: 50,
});

const style = `height: ${props.height}px`;

const fontStyle = {
  display: 'inline-block',
  fontWeight: 'bold',
  fontSize: `${Math.floor(props.height / 2)}px`,
  lineHeight: `${Math.floor(props.height / 2)}px`,
  padding: `${Math.floor(props.height / 4)}px 10px`,
  verticalAlign: 'top',
};
</script>
