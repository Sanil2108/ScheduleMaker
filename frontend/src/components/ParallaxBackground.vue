<template>
    <div class="parallax-container">
        <div
            class="shape-div"
            :class="getRandomDivObjectShape()"
            v-for="value in divObjectsKeys"
            :key="value"
            ref="divObjectElements"
        >
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ParallaxBackground',
        data() {
            return {
                divObjectElements: [],
                divObjectAttributes: [],
                NUMBER_OF_DIVS: 30,
                MIN_SCALE: 0.8,
                MAX_SCALE: 4,
                MIN_OPACITY: 0.1,
                MAX_OPACITY: 0.8,
                TRANSLATION_DELTA: 1 / 100,
                DIV_SHAPE_CLASSES: [
                    'shape-div__square',
                    'shape-div__circle',
                    'shape-div__line',
                ],
            }
        },
        computed: {
            divObjectsKeys() {
                return [...Array(this.NUMBER_OF_DIVS).keys()]
            },
        },
        mounted() {
            this.initializeDivObjects();

            document.addEventListener('mousemove', this.updateDivs)
            window.addEventListener('resize', () => {
                this.initializeDivObjects();
                this.$forceUpdate();
            });
        },
        methods: {
            getRandomDivObjectShape() {
                return this.DIV_SHAPE_CLASSES[Math.round(Math.random() * (this.DIV_SHAPE_CLASSES.length - 1))]
            },
            getRandomScaleAndOpacity() {
                const randomNumber = Math.random();

                return {
                    opacity: (randomNumber * (this.MAX_OPACITY - this.MIN_OPACITY)) + this.MIN_OPACITY,
                    scale: (randomNumber * (this.MAX_SCALE - this.MIN_SCALE)) + this.MIN_SCALE,
                }
            },
            getRandomPosition() {
                return {
                    top: Math.random() * window.innerHeight,
                    left: Math.random() * window.innerWidth,
                };
            },
            initializeDivObjects() {
                for (let i = 0; i < this.NUMBER_OF_DIVS; i += 1) {
                    
                    const div = this.$refs.divObjectElements[i];

                    const scaleAndOpacity = this.getRandomScaleAndOpacity();
                    const position = this.getRandomPosition();

                    div.style.top = position.top + 'px';
                    div.style.left = position.left + 'px';
                    div.style.transform = `scale(${scaleAndOpacity.scale})`;
                    div.style.opacity = scaleAndOpacity.opacity;

                    this.divObjectAttributes.push({
                        position,
                        scale: scaleAndOpacity.scale,
                    })
                }
            },
            getTranslationOfDiv(divObjectAttributes, event) {
                const center = {
                    x: window.innerWidth / 2,
                    y: window.innerHeight / 2,
                };
                const centerOffset = {
                    x: event.clientX - center.x,
                    y: event.clientY - center.y,
                };

                return {
                    x: centerOffset.x * divObjectAttributes.scale * this.TRANSLATION_DELTA,
                    y: centerOffset.y * divObjectAttributes.scale * this.TRANSLATION_DELTA,
                }
            },
            updateDivs(event) {
                for (let i = 0; i < this.NUMBER_OF_DIVS; i += 1) {
                    const translation = this.getTranslationOfDiv(this.divObjectAttributes[i], event);
                    this.$refs.divObjectElements[i].style.transform = `scale(${this.divObjectAttributes[i].scale}) translateX(${translation.x}px) translateY(${translation.y}px)`
                }
            },
        }
    }
</script>

<style lang="scss" scoped>
    $PRIMARY_COLOR: #18227c;
    $PRIMARY_COLOR_DARK: #0c113e;

    .parallax-container {
        background-color: $PRIMARY_COLOR_DARK;
        overflow: hidden;
        position: fixed;
        height: 100vh;
        width: 100vw;
    }

    .shape-div {
        height: 5vh;
        width: 5vh;
        display: inline-block;
        border-radius: 10px;
        background-color: transparent;
        border-style: solid;
        border-color: $PRIMARY_COLOR;
        border-width: 5px;
        position: absolute;

        &__square {

        }

        &__circle {
            border-radius: 10000000px;
        }

        &__line {
            height: 3vh;
            border-width: 0px;
            width: 0.45vh;
            border-radius: 10000px;
            background-color: $PRIMARY_COLOR;
        }
    }

</style>
