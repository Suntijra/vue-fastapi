<template>
  <v-container>
    <v-row>
      <v-col class="container-button">
        <v-btn class="item-one" color="primary" @click="showAddPartDialog">เพิ่ม Part</v-btn>
        <v-btn color="success" @click="exportData">Export Data</v-btn>
      </v-col>
      <v-col>
        <v-file-input label="Import Excel and Update" @change="importData" accept=".xlsx, .xls" />
      </v-col>
    </v-row>

    <v-data-table :headers="headers" :items="parts" class="elevation-1" :items-per-page="5">
      <template v-slot:item.actions="{ item }" >
        <v-btn class="template-action" color="red" @click="deletePart(item)">ลบ</v-btn>
        <v-btn color="yellow" @click="showEditPartDialog(item)">แก้ไข</v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="addPartDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ isEditing ? 'แก้ไข Part' : 'เพิ่ม Part' }}</span>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="partName" label="ชื่อ Part" required />
          <v-text-field v-model="changeoverTime" label="เวลาเปลี่ยน (นาที)" type="number" required />
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="savePart">{{ isEditing ? 'บันทึก' : 'เพิ่ม' }}</v-btn>
          <v-btn @click="closeDialog">ยกเลิก</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import * as XLSX from 'xlsx';
export default {
  data() {
    return {
      parts: [],
      partName: '',
      changeoverTime: 0,
      addPartDialog: false,
      isEditing: false,
      editingPart: null,
      headers: [
        { title: 'PartNo', key: 'partName', align: 'start' },
        { title: 'เวลาเปลี่ยน (นาที)', key: 'changeoverTime' },
        { title: 'การกระทำ', key: 'actions', sortable: false },
      ],
    };
  },
  methods: {
    showAddPartDialog() {
      this.isEditing = false;
      this.partName = '';
      this.changeoverTime = 0;
      this.addPartDialog = true;
    },
    showEditPartDialog(item) {
      this.isEditing = true;
      this.partName = item.partName;
      this.changeoverTime = item.changeoverTime;
      this.editingPart = item;
      this.addPartDialog = true;
    },
    closeDialog() {
      this.addPartDialog = false;
    },
    savePart() {
      if (this.isEditing) {
        // Update part
        const index = this.parts.indexOf(this.editingPart);
        console.log(index)
        this.parts[index] = { partName: this.partName, changeoverTime: this.changeoverTime }
        // this.$set(this.parts, index, { partName: this.partName, changeoverTime: this.changeoverTime });
      } else {
        // Add new part
        this.parts.push({ partName: this.partName, changeoverTime: this.changeoverTime });
      }
      this.closeDialog();
    },
    deletePart(item) {
      const index = this.parts.indexOf(item);
      this.parts.splice(index, 1);
    },
    async exportData() {
      try {
        let dataParts = this.parts
        let rows = dataParts.map((data) => {
          return [data.partName, data.changeoverTime]
        })
        const headers = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "accept": "application/json"
          },
          body: JSON.stringify({
            headers: ["PartNo", "เวลาเปลี่ยน (นาที)"],
            headers_keys: ["partName", "changeoverTime"],
            rows: rows
          })
        }
        let req = await fetch("http://localhost:3030/export-excel", headers)
        // let data = await req.json()
        let blob = await req.blob(); // รับข้อมูลเป็น blob
        // สร้างลิงก์เพื่อดาวน์โหลดไฟล์
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "exported_data.xlsx"; // ตั้งชื่อไฟล์ที่ดาวน์โหลด
        document.body.appendChild(a);
        a.click();
        a.remove(); // ลบลิงก์หลังจากดาวน์โหลด
      } catch (e) {
        console.error(e);
        alert('Failed to export data');
      }

    },
    importData(event) {
      // Get the first file from the file input
      const file = event.target.files[0]; 
      if (!file) {
        console.error("No file selected.");
        return; // Exit if no file was selected
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        // Read the data as an Excel workbook
        const workbook = XLSX.read(data, { type: 'array' });

        // Get the first sheet name
        const firstSheetName = workbook.SheetNames[0];

        // Get the first sheet data
        const worksheet = workbook.Sheets[firstSheetName];

        // Convert the sheet data to JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet);

        console.log(jsonData); // This will log the imported data as an array of objects
        alert('Importing data...');
        let partUpdate = jsonData.map((data) => {
          console.log(data)
          let arrayData = Object.values(data)
          return arrayData
        })
        partUpdate = partUpdate.map((data) => {
          return { partName: data[0], changeoverTime: parseInt(data[1]) }
        })
        this.parts = partUpdate; // Update the parts array with the imported data
      };

      // Read the file as an ArrayBuffer
      reader.readAsArrayBuffer(file); 
    },
  },
};
</script>

<style scoped>
.container-button {
  display: flex;
  align-items: center;
}

.container-button>.item-one {
  margin-right: 10px;
}
.template-action{
  margin-right: 10px;
}
/* Add your styles here */
</style>
