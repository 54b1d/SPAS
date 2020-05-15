<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>433</width>
    <height>407</height>
   </rect>
  </property>
  <property name="font">
   <font>
    <family>SolaimanLipi</family>
    <pointsize>12</pointsize>
   </font>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
  <layout class="QGridLayout" name="gridLayout">
   <item row="0" column="0">
    <widget class="QLineEdit" name="lddate">
     <property name="placeholderText">
      <string>তারিখ</string>
     </property>
    </widget>
   </item>
   <item row="2" column="0">
    <widget class="QComboBox" name="comboBox_names">
     <property name="font">
      <font>
       <family>SolaimanLipi</family>
       <pointsize>14</pointsize>
      </font>
     </property>
    </widget>
   </item>
   <item row="5" column="0">
    <widget class="QDialogButtonBox" name="buttonBox">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="standardButtons">
      <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
     </property>
    </widget>
   </item>
   <item row="4" column="0">
    <widget class="QTextEdit" name="tddesc">
     <property name="placeholderText">
      <string>মন্তব্য</string>
     </property>
    </widget>
   </item>
   <item row="3" column="0">
    <widget class="QLineEdit" name="ldamount">
     <property name="placeholderText">
      <string>টাকার পরিমান</string>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>buttonBox</sender>
   <signal>accepted()</signal>
   <receiver>Dialog</receiver>
   <slot>accept()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>248</x>
     <y>254</y>
    </hint>
    <hint type="destinationlabel">
     <x>157</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>buttonBox</sender>
   <signal>rejected()</signal>
   <receiver>Dialog</receiver>
   <slot>reject()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>316</x>
     <y>260</y>
    </hint>
    <hint type="destinationlabel">
     <x>286</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
 </connections>
</ui>
