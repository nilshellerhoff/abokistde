<template>You searched {{ $route.params.query }}</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';

const route = useRoute();

console.log(route.params.query);

const query = route.params.query;
</script>
