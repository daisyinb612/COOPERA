<template>
    <el-container class="main-container">
        <el-main class="plot">
            <el-header class="header">
                <div>PLOT</div>
            </el-header>
            <el-main class="plot">
                <el-header class="button-container-up">
                    <el-button class="button" @click="Gplot">Generate</el-button>
                    <el-button class="button" @click="AddPlot">Add</el-button>
                </el-header>
                <el-main class="plot-list-container">
                    <el-scrollbar class="plots-list">
                        <el-card v-for="(plot, index) in plots" :key="index" class="plot-item" @click="editPlot(index)">
                            <div class="plot-header">
                                <div class="scene-name">{{ plot.sceneName }}</div>
                                <div class="plot-element">{{ plot.plotElement }}</div>
                                <div class="location">{{ plot.location }}</div>
                                <div class="characters">
                                    <span v-for="character in plot.characters" :key="character">{{ character }}</span>
                                </div>
                            </div>
                            <el-input type="textarea" v-model="plot.beat" placeholder="Enter beat here..."
                                class="beat-input"></el-input>
                        </el-card>
                    </el-scrollbar>
                </el-main>
                <el-footer class="button-container-down">
                    <el-button class="button" @click="Save">Confirm</el-button>
                    <el-button class="button" @click="UploadPlot">Upload</el-button>
                </el-footer>
            </el-main>
        </el-main>
    </el-container>

    <el-dialog title="Add Plot" v-model="addDialogVisible" custom-class="dialog-content">
        <el-form :model="newPlot" label-width="100px" class="add-plot-form">
            <el-form-item label="Scene Name">
                <el-input v-model="newPlot.sceneName" autocomplete="off" />
            </el-form-item>
            <el-form-item label="Plot Element">
                <el-radio-group v-model="newPlot.plotElement">
                    <el-radio value="Exposition">Exposition</el-radio>
                    <el-radio value="Inciting Incident">Inciting Incident</el-radio>
                    <el-radio value="Conflict">Conflict</el-radio>
                    <el-radio value="Rising Action">Rising Action</el-radio>
                    <el-radio value="Climax">Climax</el-radio>
                    <el-radio value="Resolution">Falling Action</el-radio>
                    <el-radio value="Dénouement">Dénouement</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="Location">
                <el-input v-model="newPlot.location" autocomplete="off" />
            </el-form-item>
            <el-form-item label="Characters">
                <el-input v-model="newCharacter" @keyup.enter="addCharacter"
                    placeholder="Enter character and press Enter" />
                <div class="characters">
                    <el-tag v-for="(character, index) in newPlot.characters" :key="index" closable
                        @close="removeCharacter(index)">
                        {{ character }}
                    </el-tag>
                </div>
            </el-form-item>
            <el-form-item label="Beat">
                <el-input type="textarea" v-model="newPlot.beat" autocomplete="off" />
            </el-form-item>
            <el-footer class="dialog-footer">
                <el-button @click="handleAddDialogClose" class="cancel-button">Cancel</el-button>
                <el-button type="primary" @click="addNewPlot" class="confirm-button">Confirm</el-button>
            </el-footer>
        </el-form>
    </el-dialog>


</template>

<script>
import { defineComponent, ref, reactive } from 'vue';

export default defineComponent({
    name: 'GPlot',
    
    setup() {
        const addDialogVisible = ref(false);
        const plots = ref([]);
        const newPlot = reactive({
            sceneName: '',
            plotElement: '',
            location: '',
            characters: [],
            beat: ''
        });
        
        const newCharacter = ref('');

        function AddPlot() {
            addDialogVisible.value = true;
        }

        function handleAddDialogClose() {
            newPlot.sceneName = '';
            newPlot.plotElement = '';
            newPlot.location = '';
            newPlot.characters = [];
            newPlot.beat = '';
            addDialogVisible.value = false;
        }

        function addNewPlot() {
            plots.value.push({ ...newPlot });
            handleAddDialogClose();
        }

        function addCharacter() {
            if (newCharacter.value) {
                newPlot.characters.push(newCharacter.value);
                newCharacter.value = '';
            }
        }

        function removeCharacter(index) {
            newPlot.characters.splice(index, 1);
        }

        return {
            addDialogVisible,
            plots,
            newPlot,
            newCharacter,
            AddPlot,
            handleAddDialogClose,
            addNewPlot,
            addCharacter,
            removeCharacter,
        };
    }
});
</script>

<style scoped>
.main-container {
    display: flex;
    height: 88vh;
    width: 100%;
    gap: 20px;
    padding: 30px;
    overflow: hidden;
    box-sizing: border-box;
    background-color: #F4F4F4;
}

.header {
    background-color: #5973FF;
    color: white;
    text-align: center;
    line-height: 60px;
    font-size: 18px;
}

.plot {
    display: flex;
    background-color: #FFFFFF;
    flex-direction: column;
    border-radius: 20px;
    overflow: hidden;
    box-sizing: border-box;
    padding: 0;
}

.button-container-up {
    display: flex;
    justify-content: flex-start;
    padding: 5px;
    gap: 20px;
    text-align: center;
    box-sizing: border-box;
}

.button-container-down {
    display: flex;
    justify-content: flex-end;
    padding: 5px;
    gap: 20px;
    text-align: center;
    box-sizing: border-box;
}

.button {
    margin: 0 5px;
    padding: 10px 20px;
    background-color: white;
    border: 2px solid #5973FF;
    color: #BCCFFF;
    cursor: pointer;
    border-radius: 10px !important;
    transition: background-color 0.2s, color 0.2s;
}

.plot-list-container {
    flex: 1;
    overflow: hidden;
    padding: 10px;
    box-sizing: border-box;
}

.plots-list {
    height: 100%;
    overflow-y: auto;
}

.plot-item {
    margin-bottom: 10px;
    padding: 20px;
    border-radius: 10px;
    background-color: #e6e6e6;
}

.plot-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.scene-name {
    font-size: 18px;
    font-weight: bold;
}

.plot-element,
.location,
.characters {
    font-size: 14px;
}

.beat-input {
    width: 100%;
    margin-top: 10px;
}

.add-plot-form {
    padding: 10px;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    padding: 10px;
}

.cancel-button {
    background-color: #f5f5f5;
    color: #333;
}

.confirm-button {
    background-color: #5973ff;
    color: white;
}

.character-tag {
    margin-right: 5px;
}
</style>