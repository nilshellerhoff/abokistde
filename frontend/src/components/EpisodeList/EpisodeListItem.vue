<template>
  <q-card :style="{ width: `${props.width}px` }" flat>
    <ChannelRenderer
      v-if="props.showChannelHeader"
      :channel="props.episode?.publishing_channel"
      show-channel-link
    />
    <a :href="episode?.url" target="_blank" class="nolink cursor-pointer">
      <q-img
        ratio="1.778"
        :src="props.episode?.thumbnail_url"
        class="relative-position"
      >
        <div
          style="
            position: absolute;
            top: 4px;
            right: 4px;
            background-color: #ffffff88;
            border-radius: 10px;
            padding: 0;
          "
        >
          <q-btn
            v-if="props.showFavoriteButton"
            size="12px"
            color="black"
            flat
            round
            dense
            :icon="episode?.is_favorited ? 'favorite' : 'favorite_border'"
            @click.prevent="$emit('favorite')"
            style="margin: 8px"
          /><br />
          <q-btn
            v-if="showHideButtons"
            size="12px"
            color="black"
            flat
            round
            dense
            :icon="episode?.is_hidden ? 'visibility' : 'visibility_off'"
            @click.prevent="$emit('hideUnhide')"
            style="margin: 8px"
          />
        </div>
      </q-img>

      <q-item-section>
        <q-item-label
          lines="2"
          style="font-weight: bold; font-size: 14px; padding: 4px"
          >{{ props.episode.title }}
        </q-item-label>
        <q-item-label
          v-if="date"
          lines="1"
          style="font-size: 12px; padding: 4px"
        >
          <timeago :datetime="date" />
        </q-item-label>
      </q-item-section>
    </a>
  </q-card>
</template>

<script setup lang="ts">
import { Episode } from 'src/types/api';
import ChannelRenderer from 'components/ChannelRenderer.vue';

interface Props {
  episode?: Episode;
  showChannelHeader?: boolean;
  width?: number;
  showHideButtons?: boolean;
  showFavoriteButton?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showChannelHeader: false,
  width: 300,
  showHideButtons: true,
  showFavoriteButton: true,
});

const date = props.episode?.published
  ? new Date(props.episode?.published)
  : undefined;
</script>

<style>
.nolink {
  text-decoration: inherit;
  color: inherit;
}
</style>
