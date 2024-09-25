<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>ขอคิวใหม่</v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="valid">
                <v-text-field
                  v-model="licensePlate"
                  :rules="[rules.required]"
                  label="หมายเลขทะเบียนรถ"
                  required
                ></v-text-field>
                <v-select
                  v-model="selectedGate"
                  :items="gates.map(gate => gate.type)"
                  :rules="[rules.required]"
                  label="เลือกประเภทประตู"
                  required
                ></v-select>
                <v-btn @click="requestQueue">ขอคิว</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col v-for="(gate, index) in gates" :key="index" cols="12" md="4">
          <v-card>
            <v-card-title>{{ gate.type }} (ประตู {{ gate.count }})</v-card-title>
            <v-card-text>
              <v-data-table :headers="headers" :items="queueData[index]" class="elevation-1"></v-data-table>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="callNextVehicle(index)">เรียกรถเข้า</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      
      <v-alert v-if="nextQueue" type="info">
        คิวถัดไป: {{ nextQueue.licensePlate }} เวลา: {{ nextQueue.time }}
      </v-alert>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        licensePlate: '',
        selectedGate: null,
        valid: false,
        rules: {
          required: value => !!value || 'จำเป็นต้องกรอก'
        },
        gates: [
          { type: 'ประเภทที่ 1 (รถ 10 ล้อ)', count: 2 },
          { type: 'ประเภทที่ 2 (รถ 6 ล้อ)', count: 4 },
          { type: 'ประเภทที่ 3 (รถกระบะ)', count: 2 }
        ],
        headers: [
          { text: 'หมายเลขรถ', value: 'licensePlate' },
          { text: 'เวลาเรียกคิว', value: 'time' }
        ],
        queueData: [[], [], []],
        nextQueue: null
      }
    },
    methods: {
      requestQueue() {
        const gateIndex = this.gates.findIndex(gate => gate.type === this.selectedGate);
        const timeNow = new Date().toLocaleString();
        if (gateIndex !== -1 && this.licensePlate) {
          this.queueData[gateIndex].push({
            licensePlate: this.licensePlate,
            time: timeNow
          });
          this.licensePlate = '';
          this.selectedGate = null;
          this.$refs.form.reset();
        }
      },
      callNextVehicle(gateIndex) {
        const vehicle = this.queueData[gateIndex].shift();
        if (vehicle) {
          this.nextQueue = vehicle;
        }
      }
    }
  }
  </script>
  