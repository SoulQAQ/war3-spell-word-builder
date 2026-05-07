<template>
  <div class="spell-container" :style="{fontSize: (fontSize || 12) + 'px'}">
    <div v-if="module === '学习'">
      <p style="margin-bottom: 3px;">
        学习 <span :style="{color: colorConfig.learnLevel}">{{ spellData.lv || '%d' }}级</span>
        {{ spellData.name || '技能名称' }}
        <span v-if="spellData.hotKey">
          (<span :style="{color: colorConfig.hotKey}">{{ spellData.hotKey }}</span>)
        </span>
      </p>
      <hr>
      <p style="margin-top: 7px;">
        {{ spellData.effect }}
        <br/>
        <span v-if="spellData.nature">
          <br><span :style="{color: colorConfig.nature}">{{ spellData.nature }}</span><br>
        </span>
        <br/>
        <span v-if="p.val" v-for="(p,i) in learnPros" :key="i">
          <span :style="{color: colorConfig.property}">
            {{ p.name }}：
          </span>
          {{ p.key ? `<${spellData.id},${p.key}${p.lv}${p.r ? ',%' : ''}>` : (p.val || '(null)') }}
          <br>
        </span>
        <span v-if="spellData.updateWord && spellData.updateWord.vals"
              v-for="(l,i) in spellData.updateWord.vals">
          <br>
          <span :style="{color: colorConfig.learnUpdateLevel}">{{ (i + 1) }}级</span> -
          {{ spellData.updateWord.text.format(l) }}
          {{ spellData.updateWord.text.endsWith("。") ? null : '。' }}
        </span>
      </p>
    </div>
    <div v-if="module === '普通'">
      <p style="margin-bottom: 3px;">
        {{ spellData.name || '技能名称' }}
        <span v-if="spellData.hotKey">(<span :style="{color: colorConfig.hotKey}">{{ spellData.hotKey }}</span>)</span>
        -
        [<span :style="{color: colorConfig.learnLevel}">{{ spellData.lv || '1' }}级</span>]
      </p>
      <hr>
      <p style="margin-top: 7px;">
        {{ spellData.normalWord.text.format(spellData.normalWord.vals[spellData.lv - 1]) }}
        {{ spellData.normalWord.text.length === 0 || spellData.normalWord.text.endsWith("。") ? null : '。' }}
        <br/>
        <span v-if="spellData.nature">
          <br><span :style="{color: colorConfig.nature}">{{ spellData.nature }}</span><br>
        </span>
        <br v-if="normalPros.length > 0">
        <span v-if="p.val" v-for="(p,i) in normalPros" :key="i">
          <span :style="{color: colorConfig.property}">
            {{ p.name }}：
          </span>
          {{ p.key ? `<${spellData.id},${p.key}${p.lv}${p.r ? ',%' : ''}>` : (p.val || '(null)') }}
          <br>
        </span>
      </p>
    </div>
  </div>
</template>

<script>

const default_spell_data = {
  id: "A000",
  lv: "1",
  name: "名称丢失",
  hotKey: "Q",
  effect: "法术效果丢失",
  pros: [],
  updateWord: undefined,
  nature: undefined,
  normalWord: undefined,
}

export default {
  name: 'Spell',
  props: {
    module: {
      default: () => '学习',
      type: String
    },
    spellData: {
      default: () => Object.assign({}, default_spell_data),
      type: Object
    },
    colorConfig: {
      default: () => {
      },
      type: Object
    },
    fontSize: Number
  },
  components: {},
  data() {
    return {}
  },
  computed: {
    normalPros() {
      return this.spellData.pros.filter(e => e.name && e.name !== '法力消耗')
    },
    learnPros() {
      return this.spellData.pros.filter(e => e.name)
    }
  },
  watch: {},
  created() {

  },
  mounted() {
  },
  methods: {}
}
</script>

<style scoped lang="scss">
.spell-container {
  text-align: left;
  font-weight: bold !important;
  background-color: rgba(0, 0, 0, .75);
  color: #ffffff;
  border-radius: 5px;
  padding: 3%;
  box-sizing: border-box;
}
</style>
