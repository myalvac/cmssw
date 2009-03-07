import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("L1ConfigWritePayloadDummy")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cout.placeholder = cms.untracked.bool(False)
process.MessageLogger.cout.threshold = cms.untracked.string('DEBUG')
process.MessageLogger.debugModules = cms.untracked.vstring('*')

options = VarParsing.VarParsing()
options.register('tagBase',
                 'CRAFT', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "IOV tags = object_{tagBase}_hlt")
options.register('orconConnect',
                 'sqlite_file:l1config.db', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Connection string for ORCON")
options.register('orconAuth',
                 '.', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Authentication path for ORCON")
options.parseArguments()

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
process.source = cms.Source("EmptyIOVSource",
    timetype = cms.string('runnumber'),
    firstValue = cms.uint64(1),
    lastValue = cms.uint64(1),
    interval = cms.uint64(1)
)

# Generate dummy L1TriggerKey and L1TriggerKeyList
process.load("CondTools.L1Trigger.L1TriggerKeyDummy_cff")
process.L1TriggerKeyDummy.objectKeys = cms.VPSet()
process.L1TriggerKeyDummy.tscKey = cms.string('')

# Use dummy producer to initialize DB on the first time ONLY.
process.load("CondTools.L1Trigger.L1TriggerKeyListDummy_cff")

# writer modules
process.load("CondTools.L1Trigger.L1CondDBPayloadWriter_cfi")
process.L1CondDBPayloadWriter.L1TriggerKeyListTag = cms.string('L1TriggerKeyList_' + options.tagBase + '_hlt')
process.L1CondDBPayloadWriter.offlineDB = cms.string(options.orconConnect)
process.L1CondDBPayloadWriter.offlineAuthentication = cms.string(options.orconAuth)

process.p = cms.Path(process.L1CondDBPayloadWriter)
