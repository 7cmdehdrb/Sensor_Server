/**
 *  Copyright 2014 SmartThings
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
metadata {
    // Automatically generated. Make future change here.
    definition (name: "ARDUINO SENSOR", namespace: "SoYu", author: "SoYu", mnmn: "SoYu") {
    	capability "Refresh"			
		capability "Illuminance Measurement"    //illuminance
    }

    preferences {
        input "KEY", "text", type: "text", title: "ID", description: "INPUT KEY", required: true
    }
}


def installed() {
    refresh()
}

def uninstalled() {
    unschedule()
}

def updated() {
    refresh()
}

def refresh() {
    pollSensor()

    runEvery10Minutes(pollSensor)
}


def pollSensor() {
    log.debug "pollSensor()"

    def params = [
        uri: "http://7cmdehdrb.iptime.org:14111/light_sensor?key=${settings.KEY}",
        contentType: 'application/json'
    ]

    try {
        httpGet(params) {resp ->
            if (resp.status == 200) {

                if (resp.data.success == false){
                    throw new Exception("INVALID KEY")
                }

                log.debug "light_value: ${resp.data.data}"
                sendEvent(name: "illuminance", value: resp.data.data, unit: "ohm")

            } else {
                log.debug "HTTP STATE ERROR: ${resp.status}"
            }
        }
    } catch (e) {
        log.debug "UNKNOWN ERROR: ${e}"
    }
}

